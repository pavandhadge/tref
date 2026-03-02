from __future__ import annotations

import json
import os
import threading
from pathlib import Path

import faiss
import numpy as np
from fastembed import TextEmbedding

from tref.config import EMBED_MODEL
from tref.models import SearchResult


def _build_embedder(model_name: str = EMBED_MODEL) -> TextEmbedding:
    # Prefer GPU execution provider when available in runtime; fallback to CPU.
    try:
        return TextEmbedding(model_name=model_name, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    except TypeError:
        # Older fastembed versions may not expose providers argument.
        return TextEmbedding(model_name=model_name)
    except Exception:
        return TextEmbedding(model_name=model_name)


class Retriever:
    _embedder: TextEmbedding | None = None
    _cache: dict[str, "Retriever"] = {}
    _lock = threading.Lock()

    def __init__(self, index_dir: Path, model_name: str = EMBED_MODEL):
        self.index_dir = index_dir
        self.index = faiss.read_index(str(index_dir / "index.faiss"))
        # If available FAISS can use multiple CPU threads for search.
        try:
            faiss.omp_set_num_threads(max(1, os.cpu_count() or 1))
        except Exception:
            pass

        with (index_dir / "chunks.jsonl").open("r", encoding="utf-8") as fh:
            # Keep only fields needed at query time to reduce memory.
            self.chunks = []
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
                return inst
            inst = cls(index_dir=index_dir, model_name=model_name)
            cls._cache[key] = inst
            return inst

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        vector = np.array(list(self._embedder.embed([query])), dtype="float32")
        faiss.normalize_L2(vector)

        scores, indices = self.index.search(vector, top_k)
        out: list[SearchResult] = []

        for score, idx in zip(scores[0], indices[0], strict=False):
            if idx < 0:
                continue
            chunk = self.chunks[int(idx)]
            out.append(
                SearchResult(
                    score=float(score),
                    text=chunk["text"],
                    citation=chunk["citation"],
                    library=chunk["library"],
                    version=chunk["version"],
                    item=chunk["item"],
                    signature=chunk["signature"],
                )
            )
        return out
