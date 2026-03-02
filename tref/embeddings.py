from __future__ import annotations

from fastembed import TextEmbedding

from tref.config import EMBED_MODEL


class EmbeddingManager:
    """Compatibility wrapper around fastembed for lightweight CPU embeddings."""

    _model: TextEmbedding | None = None

    def __init__(self, model_name: str = EMBED_MODEL) -> None:
        self.model_name = model_name
        if EmbeddingManager._model is None:
            EmbeddingManager._model = TextEmbedding(model_name=self.model_name)

    def encode_query(self, query: str):
        return list(self._model.embed([query]))[0]

    def encode_batch(self, texts: list[str]):
        return list(self._model.embed(texts))
