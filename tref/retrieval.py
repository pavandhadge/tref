from __future__ import annotations

import json
import os
import re
import threading
from collections import OrderedDict
from pathlib import Path

import faiss
import numpy as np
from fastembed import TextEmbedding

from tref.config import EMBED_MODEL
from tref.models import SearchResult

TOKEN_RE = re.compile(r"[a-zA-Z0-9_.-]+")
MAX_RETRIEVER_CACHE = 8


def _build_embedder(model_name: str = EMBED_MODEL) -> TextEmbedding:
    try:
        return TextEmbedding(model_name=model_name, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    except TypeError:
        return TextEmbedding(model_name=model_name)
    except Exception:
        return TextEmbedding(model_name=model_name)


def _tokenize(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


class Retriever:
    _embedder: TextEmbedding | None = None
    _cache: "OrderedDict[str, Retriever]" = OrderedDict()
    _lock = threading.Lock()

    def __init__(self, index_dir: Path, model_name: str = EMBED_MODEL):
        self.index_dir = index_dir
        self.index = faiss.read_index(str(index_dir / "index.faiss"))
        try:
            faiss.omp_set_num_threads(max(1, os.cpu_count() or 1))
        except Exception:
            pass

        self.chunks = []
        meta_path = index_dir / "meta.json"
        self.index_meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
        with (index_dir / "chunks.jsonl").open("r", encoding="utf-8") as fh:
            for line in fh:
                raw = json.loads(line)
                self.chunks.append(
                    {
                        "text": raw["text"],
                        "citation": raw["citation"],
                        "library": raw["library"],
                        "version": raw["version"],
                        "item": raw["item"],
                        "signature": raw["signature"],
                        "section": raw.get("section", ""),
                        "query_text": f"{raw['item']} {raw['signature']} {raw['text']}",
                    }
                )

        if Retriever._embedder is None:
            Retriever._embedder = _build_embedder(model_name=model_name)

    @classmethod
    def get(cls, index_dir: Path, model_name: str = EMBED_MODEL) -> "Retriever":
        key = str(index_dir.resolve())
        with cls._lock:
            inst = cls._cache.get(key)
            if inst is not None:
                cls._cache.move_to_end(key)
                return inst
            inst = cls(index_dir=index_dir, model_name=model_name)
            cls._cache[key] = inst
            while len(cls._cache) > MAX_RETRIEVER_CACHE:
                cls._cache.popitem(last=False)
            return inst

    def _hybrid_scores(self, query: str, scores: np.ndarray, indices: np.ndarray) -> list[tuple[float, int]]:
        q_tokens = _tokenize(query)
        ranked: list[tuple[float, int]] = []
        for sem_score, idx in zip(scores, indices, strict=False):
            if idx < 0:
                continue
            doc = self.chunks[int(idx)]
            d_tokens = _tokenize(doc["query_text"])
            overlap = len(q_tokens & d_tokens) / max(1, len(q_tokens))
            # lightweight hybrid rank; semantic remains dominant.
            hybrid = (0.85 * float(sem_score)) + (0.15 * float(overlap))
            ranked.append((hybrid, int(idx)))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return ranked

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        vector = np.array(list(self._embedder.embed([query])), dtype="float32")
        faiss.normalize_L2(vector)

        # Over-fetch for lexical reranking.
        fetch_k = min(max(top_k * 4, top_k), len(self.chunks))
        scores, indices = self.index.search(vector, fetch_k)
        ranked = self._hybrid_scores(query, scores[0], indices[0])[:top_k]

        out: list[SearchResult] = []
        for score, idx in ranked:
            chunk = self.chunks[idx]
            out.append(
                SearchResult(
                    score=float(score),
                    text=chunk["text"],
                    citation=chunk["citation"],
                    library=chunk["library"],
                    version=chunk["version"],
                    item=chunk["item"],
                    signature=chunk["signature"],
                    section=chunk.get("section", ""),
                )
            )
        return out
