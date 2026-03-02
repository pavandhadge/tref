from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from tref.config import DEFAULT_TOP_K, INDEX_ROOT, OLLAMA_URL
from tref.kb import detect_library_from_query, resolve_version, split_inline_library_version
from tref.models import AskResponse
from tref.retrieval import Retriever
from tref.updater import ensure_index_exists, freshness_status


def _ollama_answer(query: str, contexts: list[dict[str, Any]], model: str) -> str:
    context_blob = "\n\n".join(
        f"[{idx + 1}] {ctx['citation']}\n{ctx['text']}" for idx, ctx in enumerate(contexts)
    )
    prompt = (
        "You are a strict documentation assistant. "
        "Answer only from provided context. If insufficient, say so.\n\n"
        f"Question:\n{query}\n\n"
        f"Context:\n{context_blob}\n\n"
        "Answer with concise, technical guidance and cite source numbers like [1], [2]."
    )
    payload = {"model": model, "prompt": prompt, "stream": False}
    response = httpx.post(OLLAMA_URL, json=payload, timeout=60.0)
    response.raise_for_status()
    data = response.json()
    return str(data.get("response", "")).strip()


def ask(
    query: str,
    library: str | None = None,
    version: str | None = None,
    top_k: int = DEFAULT_TOP_K,
    json_mode: bool = False,
    llm: bool = False,
    llm_model: str = "llama3.1:8b-instruct",
    strict_fresh: bool = False,
    index_root: Path | None = None,
) -> dict[str, Any] | AskResponse:
    clean_query = query.strip()
    if not clean_query:
        raise ValueError("query must not be empty")
    base_dir = index_root.expanduser().resolve() if index_root else INDEX_ROOT

    parsed_library, parsed_version, stripped_query = split_inline_library_version(clean_query)
    autodetected = False
    if library is None and parsed_library:
        library = parsed_library
        version = version or parsed_version
        clean_query = stripped_query

    if not library:
        guessed_library = detect_library_from_query(clean_query, index_root=base_dir)
        if not guessed_library:
            raise ValueError(
                "library could not be auto-detected. Use 'library@version query' or --library."
            )
        library = guessed_library
        autodetected = True

    resolved_version = resolve_version(library, version, index_root=base_dir)
    index_dir = ensure_index_exists(
        library,
        resolved_version,
        index_root=base_dir,
        ensure_fresh=True,
        strict_fresh=strict_fresh,
    )

    retriever = Retriever.get(index_dir=index_dir)
    hits = retriever.search(clean_query, top_k=top_k)
    fresh = freshness_status()
    warnings: list[str] = []
    if autodetected:
        warnings.append(f"Library auto-detected as '{library}'.")
    if not fresh.get("fresh", False):
        warnings.append("Index freshness check failed or is stale. Run `tref update`.")
    if fresh.get("verified") is False:
        warnings.append("Index verification is missing/failed for current local snapshot.")

    response = AskResponse(
        library=library,
        version=resolved_version,
        query=clean_query,
        results=hits,
        autodetected_library=autodetected,
        freshness=fresh,
        warnings=warnings,
    )

    if llm:
        response.answer = _ollama_answer(clean_query, [r.to_dict() for r in hits], llm_model)

    if json_mode:
        return response.to_dict()
    return response
