from __future__ import annotations

from pathlib import Path

from tref.retrieval import Retriever


class SearchManager:
    """Compatibility wrapper that delegates semantic search to Retriever."""

    def __init__(self, index_dir: Path):
        self.retriever = Retriever(index_dir=index_dir)

    def semantic_search(self, query: str, top_k: int = 5):
        return [r.to_dict() for r in self.retriever.search(query, top_k=top_k)]
