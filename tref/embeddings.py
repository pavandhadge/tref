import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from tref.config import DEFAULT_MODEL, CHUNK_SIZE, EMBEDDING_DIM, get_device

class EmbeddingManager:
    _model_instance = None
    _tokenizer_instance = None

    def __init__(self):
        self.device = get_device()
        self._load_model()

    @classmethod
    def _load_model(cls):
        if cls._model_instance is None:
            device = get_device()
            cls._model_instance = AutoModel.from_pretrained(
                DEFAULT_MODEL,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True
            ).eval().to(device)
        if cls._tokenizer_instance is None:
            cls._tokenizer_instance = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
        return cls._model_instance, cls._tokenizer_instance

    def encode_query(self, query: str) -> np.ndarray:
        model, tokenizer = self._load_model()
        inputs = tokenizer(
            query,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        ).to(self.device)
        with torch.no_grad():
            outputs = model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
            embedding = embedding.astype(np.float16)
        return embedding

    def encode_batch(self, texts):
        model, tokenizer = self._load_model()
        embeddings = []
        for i in range(0, len(texts), CHUNK_SIZE):
            chunk = texts[i:i + CHUNK_SIZE]
            inputs = tokenizer(
                chunk,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=256
            ).to(self.device)
            with torch.no_grad():
                outputs = model(**inputs)
                chunk_emb = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                chunk_emb = chunk_emb / np.linalg.norm(chunk_emb, axis=1, keepdims=True)
                embeddings.append(chunk_emb.astype(np.float16))
        return np.vstack(embeddings) 