from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from tref.config import DEFAULT_FRESHNESS_POLICY, DEFAULT_TOP_K, INDEX_ROOT, OLLAMA_URL
from tref.errors import DetectionError
from tref.kb import detect_library_from_query, resolve_version, split_inline_library_version
from tref.models import AskResponse
from tref.retrieval import Retriever
from tref.updater import ensure_index_exists, freshness_status


def _build_guidance(hits: list) -> dict[str, Any]:
    if not hits:
        return {
            "command_or_function": None,
            "signature": None,
            "returns": None,
            "confidence": 0.0,
            "examples": [],
            "cautions": [],
            "citations": [],
        }

    top = hits[0]
    examples = []
    cautions = []
    citations = []
    returns = None

    for hit in hits:
        citations.append({"citation": hit.citation, "section": hit.section, "item": hit.item})
        section = (hit.section or "").lower()
        if section == "examples":
            examples.append({"text": hit.text, "citation": hit.citation, "confidence": hit.score})
        if section in {"gotchas / version notes", "cautions", "warnings"}:
            cautions.append({"text": hit.text, "citation": hit.citation, "confidence": hit.score})
        if section == "returns" and returns is None:
            returns = {"text": hit.text, "citation": hit.citation}

    return {
        "command_or_function": top.item,
        "signature": top.signature,
        "returns": returns,
        "confidence": top.score,
        "examples": examples[:3],
        "cautions": cautions[:3],
        "citations": citations[:8],
    }


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
    freshness_policy: str = DEFAULT_FRESHNESS_POLICY,
    no_autodetect: bool = False,
    index_root: Path | None = None,
) -> dict[str, Any] | AskResponse:
    clean_query = query.strip()
    if not clean_query:
        raise ValueError("query must not be empty")
    base_dir = index_root.expanduser().resolve() if index_root else INDEX_ROOT

    parsed_library, parsed_version, stripped_query = split_inline_library_version(clean_query)
    autodetected = False
    warnings: list[str] = []

    if library is None and parsed_library:
        library = parsed_library
        version = version or parsed_version
        clean_query = stripped_query

    if library is None and no_autodetect:
        raise DetectionError("DETECT_DISABLED", "Library must be provided when --no-autodetect is enabled")

    if not library:
        guessed_library, candidates = detect_library_from_query(clean_query, index_root=base_dir)
        if not guessed_library:
            raise DetectionError(
                "DETECT_AMBIGUOUS",
                f"Library could not be auto-detected confidently. Top candidates: {candidates}",
            )
        library = guessed_library
        autodetected = True
        warnings.append(f"Library auto-detected as '{library}'.")

    freshness = freshness_status()
    policy = freshness_policy.lower().strip()
    if policy not in {"strict", "warn", "offline-only"}:
        raise ValueError("freshness_policy must be one of: strict, warn, offline-only")

    if policy == "offline-only":
        ensure_fresh = False
        strict_fresh_effective = False
    elif policy == "strict":
        ensure_fresh = True
        strict_fresh_effective = True
    else:  # warn
        ensure_fresh = True
        strict_fresh_effective = strict_fresh

    resolved_version = resolve_version(library, version, index_root=base_dir)
    index_dir = ensure_index_exists(
        library,
        resolved_version,
        index_root=base_dir,
        ensure_fresh=ensure_fresh,
        strict_fresh=strict_fresh_effective,
    )

    retriever = Retriever.get(index_dir=index_dir)
    hits = retriever.search(clean_query, top_k=top_k)
    freshness = freshness_status()

    if not freshness.get("fresh", False):
        warnings.append("Index freshness check failed or is stale. Run `tref update`.")
    if freshness.get("verified") is False:
        warnings.append("Index verification is missing/failed for current local snapshot.")

    provenance = {
        "index_dir": str(index_dir),
        "embedding_model": retriever.index_meta.get("embedding_model"),
        "kb_commit": retriever.index_meta.get("kb_commit"),
        "build_hash": retriever.index_meta.get("build_hash"),
        "builder_version": retriever.index_meta.get("builder_version"),
        "freshness_policy": policy,
    }

    response = AskResponse(
        library=library,
        version=resolved_version,
        query=clean_query,
        results=hits,
        autodetected_library=autodetected,
        freshness=freshness,
        provenance=provenance,
        guidance=_build_guidance(hits),
        warnings=warnings,
    )

    if llm:
        response.answer = _ollama_answer(clean_query, [r.to_dict() for r in hits], llm_model)

    if json_mode:
        return response.to_dict()
    return response
