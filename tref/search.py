import numpy as np
from typing import List, Dict
from tref.embeddings import EmbeddingManager
from tref.config import TOP_K, CACHE_SIZE

class SearchManager:
    def __init__(self, embeddings, metadata):
        self.embeddings = embeddings
        self.metadata = metadata
        self._tool_indices = {}
        self._query_cache = {}
        self.embedding_manager = EmbeddingManager()

    def _fast_cosine_similarity(self, query: np.ndarray, targets: np.ndarray) -> np.ndarray:
        return np.dot(targets, query.T).flatten()

    def _get_tool_indices(self, tool: str) -> np.ndarray:
        if tool in self._tool_indices:
            return self._tool_indices[tool]
        indices = [
            i for i, m in enumerate(self.metadata)
            if m['tool'].lower() == tool.lower()
        ]
        self._tool_indices[tool] = indices
        return indices

    def semantic_search(self, tool: str, query: str, top_k: int = TOP_K) -> List[Dict]:
        if self.embeddings is None or self.metadata is None:
            raise ValueError("Embeddings or metadata not loaded")
        relevant_indices = self._get_tool_indices(tool)
        if not relevant_indices:
            return []
        relevant_embeddings = self.embeddings[relevant_indices]
        if query in self._query_cache:
            query_embedding = self._query_cache[query]
        else:
            query_embedding = self.embedding_manager.encode_query(query)
            if len(self._query_cache) >= CACHE_SIZE:
                self._query_cache.pop(next(iter(self._query_cache)))
            self._query_cache[query] = query_embedding
        scores = self._fast_cosine_similarity(query_embedding, relevant_embeddings)
        if len(scores) <= top_k:
            top_indices = np.argsort(scores)[::-1]
        else:
            top_indices = np.argpartition(scores, -top_k)[-top_k:]
            top_indices = top_indices[np.argsort(scores[top_indices])[::-1]]
        return [{
            'name': self.metadata[relevant_indices[i]]['name'],
            'command': self.metadata[relevant_indices[i]]['command'],
            'explanation': self.metadata[relevant_indices[i]]['explanation'],
            'score': float(scores[i])
        } for i in top_indices] 