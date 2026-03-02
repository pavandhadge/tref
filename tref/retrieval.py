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
MAX_QUERY_VECTOR_CACHE = 256


def _build_embedder(model_name: str = EMBED_MODEL) -> TextEmbedding:
    try:
        return TextEmbedding(model_name=model_name, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    except TypeError:
        return TextEmbedding(model_name=model_name)
    except Exception:
        return TextEmbedding(model_name=model_name)


def _tokenize(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def _strip_chunk_scaffold(text: str) -> str:
    lines = text.splitlines()
    if len(lines) >= 3 and lines[0].startswith("# ") and lines[1].startswith("## "):
        cleaned = "\n".join(lines[2:]).strip()
        return cleaned if cleaned else text.strip()
    return text.strip()


def infer_query_intent(query: str) -> str:
    q = query.lower()
    if any(term in q for term in ("caution", "warning", "danger", "safe", "risk", "gotcha")):
        return "risk"
    if any(term in q for term in ("example", "sample", "demo", "how to")):
        return "example"
    if any(term in q for term in ("alternative", "other way", "another way", "options")):
        return "alternatives"
    if any(term in q for term in ("overview", "what is", "what does", "documentation", "full doc")):
        return "overview"
    return "default"


class Retriever:
    _embedder: TextEmbedding | None = None
    _cache: "OrderedDict[str, Retriever]" = OrderedDict()
    _lock = threading.Lock()
    _query_vector_cache: "OrderedDict[str, np.ndarray]" = OrderedDict()

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
                alias_text = " ".join(raw.get("aliases", []))
                intent_text = raw.get("intent", "")
                query_text = f"{raw['item']} {raw['signature']} {alias_text} {intent_text} {raw['text']}"
                chunk_id = str(raw.get("id", ""))
                try:
                    order = int(chunk_id.rsplit("::", 1)[-1])
                except Exception:
                    order = 0
                self.chunks.append(
                    {
                        "id": chunk_id,
                        "order": order,
                        "text": raw["text"],
                        "citation": raw["citation"],
                        "library": raw["library"],
                        "version": raw["version"],
                        "item": raw["item"],
                        "type": raw.get("type", ""),
                        "signature": raw["signature"],
                        "section": raw.get("section", ""),
                        "source_url": raw.get("source_url"),
                        "source_title": raw.get("source_title"),
                        "query_text": query_text,
                        "query_tokens": _tokenize(query_text),
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

    def _section_boost(self, section: str, intent: str) -> float:
        sec = section.lower()
        if intent == "risk" and sec in {"gotchas / version notes", "warnings", "cautions"}:
            return 0.18
        if intent == "example" and sec in {"examples", "use when"}:
            return 0.14
        if intent == "alternatives" and sec == "alternatives":
            return 0.16
        if intent == "overview" and sec in {"what it does", "use when", "signature"}:
            return 0.12
        if intent == "default" and sec in {"what it does", "signature", "parameters"}:
            return 0.06
        return 0.0

    def _hybrid_scores(
        self, query: str, scores: np.ndarray, indices: np.ndarray, intent: str = "default"
    ) -> list[tuple[float, int]]:
        q_tokens = _tokenize(query)
        ranked: list[tuple[float, int]] = []
        for sem_score, idx in zip(scores, indices, strict=False):
            if idx < 0:
                continue
            doc = self.chunks[int(idx)]
            d_tokens = doc["query_tokens"]
            overlap = len(q_tokens & d_tokens) / max(1, len(q_tokens))
            section_bonus = self._section_boost(str(doc.get("section", "")), intent)
            # Intent-aware lightweight hybrid rank; semantic remains dominant.
            hybrid = (0.78 * float(sem_score)) + (0.14 * float(overlap)) + (0.08 * float(section_bonus))
            ranked.append((hybrid, int(idx)))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return ranked

    @classmethod
    def _query_vector(cls, query: str) -> np.ndarray:
        with cls._lock:
            vec = cls._query_vector_cache.get(query)
            if vec is not None:
                cls._query_vector_cache.move_to_end(query)
                return vec

        vector = np.array(list(cls._embedder.embed([query])), dtype="float32")
        faiss.normalize_L2(vector)

        with cls._lock:
            cls._query_vector_cache[query] = vector
            while len(cls._query_vector_cache) > MAX_QUERY_VECTOR_CACHE:
                cls._query_vector_cache.popitem(last=False)
        return vector

    def search(self, query: str, top_k: int = 5, intent: str | None = None) -> list[SearchResult]:
        query_intent = intent or infer_query_intent(query)
        vector = self._query_vector(query)

        # Over-fetch for lexical reranking.
        fetch_k = min(max(top_k * 4, top_k), len(self.chunks))
        scores, indices = self.index.search(vector, fetch_k)
        ranked = self._hybrid_scores(query, scores[0], indices[0], intent=query_intent)[:top_k]

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
                    source_url=chunk.get("source_url"),
                    source_title=chunk.get("source_title"),
                )
            )
        return out

    def item_document(self, item: str) -> list[dict[str, str]]:
        sections = [chunk for chunk in self.chunks if chunk["item"] == item]
        sections.sort(key=lambda c: int(c.get("order", 0)))
        out: list[dict[str, str]] = []
        for section in sections:
            out.append(
                {
                    "section": section.get("section", ""),
                    "text": _strip_chunk_scaffold(section.get("text", "")),
                    "doc_url": section.get("source_url"),
                }
            )
        return out
