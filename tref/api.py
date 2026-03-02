from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from tref.config import DEFAULT_FRESHNESS_POLICY, DEFAULT_TOP_K, INDEX_ROOT, OLLAMA_URL
from tref.errors import DetectionError
from tref.kb import detect_library_from_query, resolve_version_with_reason, split_inline_library_version
from tref.models import AskResponse
from tref.retrieval import Retriever, infer_query_intent
from tref.updater import ensure_index_exists, freshness_status

RISK_TERMS = {
    "delete",
    "drop",
    "remove",
    "reset",
    "force",
    "overwrite",
    "rebase",
    "danger",
    "caution",
    "warning",
}
EXAMPLE_TERMS = {"example", "examples", "sample", "demo", "how to", "show"}
OVERVIEW_TERMS = {"overview", "full doc", "documentation", "all options", "all ways", "complete"}


def _query_flags(query: str) -> dict[str, bool]:
    q = query.lower()
    return {
        "risk_focus": any(term in q for term in RISK_TERMS),
        "example_focus": any(term in q for term in EXAMPLE_TERMS),
        "overview_focus": any(term in q for term in OVERVIEW_TERMS),
    }


def _strip_chunk_scaffold(text: str) -> str:
    lines = text.splitlines()
    # Chunks are stored as:
    #   # <item>
    #   ## <section>
    #   <section content>
    if len(lines) >= 3 and lines[0].startswith("# ") and lines[1].startswith("## "):
        cleaned = "\n".join(lines[2:]).strip()
        return cleaned if cleaned else text.strip()
    return text.strip()


def _extract_list_lines(text: str, limit: int = 8) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            lines.append(line[2:].strip())
        elif len(line) > 2 and line[0].isdigit() and line[1] == ".":
            lines.append(line[2:].strip())
        if len(lines) >= limit:
            break
    return lines


def _extract_code_blocks(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    blocks: list[tuple[str, str]] = []
    in_code = False
    lang = ""
    current: list[str] = []
    for raw in lines:
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            if in_code:
                body = "\n".join(current).strip()
                if body:
                    blocks.append((lang, body))
                current = []
                in_code = False
                lang = ""
            else:
                fence = line.strip()
                lang = fence[3:].strip().split()[0] if len(fence) > 3 else ""
                in_code = True
            continue
        if in_code:
            current.append(line)
    return blocks


def _normalize_language(lang: str | None) -> str:
    value = (lang or "").strip().lower()
    aliases = {
        "js": "javascript",
        "node": "javascript",
        "ts": "typescript",
        "py": "python",
        "sh": "bash",
        "shell": "bash",
    }
    return aliases.get(value, value)


def _augment_guidance_from_sections(guidance: dict[str, Any], sections: list[dict[str, Any]]) -> dict[str, Any]:
    if not guidance:
        return guidance

    def _append_unique(target: list[dict[str, Any]], candidate: dict[str, Any], key: str = "text") -> None:
        val = str(candidate.get(key, "")).strip()
        if not val:
            return
        for existing in target:
            if str(existing.get(key, "")).strip() == val:
                return
        target.append(candidate)

    examples = list(guidance.get("examples") or [])
    cautions = list(guidance.get("cautions") or [])
    alternatives = list(guidance.get("alternatives") or [])
    citations = list(guidance.get("citations") or [])
    seen_urls = {str(c.get("url", "")).strip() for c in citations if c.get("url")}

    for sec in sections:
        name = str(sec.get("section", "")).strip().lower()
        text = str(sec.get("text", "")).strip()
        doc_url = sec.get("doc_url")
        if not text:
            continue
        if doc_url and doc_url not in seen_urls:
            citations.append({"url": doc_url, "title": guidance.get("command_or_function") or "reference"})
            seen_urls.add(str(doc_url))
        if name == "examples":
            blocks = _extract_code_blocks(text)
            if blocks:
                for lang, code in blocks:
                    _append_unique(
                        examples,
                        {
                            "text": f"```{lang}\n{code}\n```" if lang else f"```\n{code}\n```",
                            "doc_url": doc_url,
                            "confidence": guidance.get("confidence", 0),
                            "language": _normalize_language(lang),
                        },
                    )
            else:
                _append_unique(examples, {"text": text, "doc_url": doc_url, "confidence": guidance.get("confidence", 0)})
        elif name in {"gotchas / version notes", "cautions", "warnings"}:
            lines = _extract_list_lines(text, limit=20)
            if lines:
                for line in lines:
                    _append_unique(cautions, {"text": line, "doc_url": doc_url, "confidence": guidance.get("confidence", 0)})
            else:
                _append_unique(cautions, {"text": text, "doc_url": doc_url, "confidence": guidance.get("confidence", 0)})
        elif name == "alternatives":
            lines = _extract_list_lines(text, limit=20)
            for line in lines:
                _append_unique(
                    alternatives,
                    {"name": line, "why": "Alternative approach from official docs context.", "doc_url": doc_url},
                    key="name",
                )

    guidance["examples"] = examples
    guidance["cautions"] = cautions
    guidance["alternatives"] = alternatives
    guidance["citations"] = citations
    return guidance


def _extract_structured_fields_from_sections(guidance: dict[str, Any], sections: list[dict[str, Any]]) -> dict[str, Any]:
    description = ""
    parameters: list[dict[str, str]] = []
    returns_text = ""
    source_url = ""
    source_title = ""
    last_updated = ""

    for sec in sections:
        name = str(sec.get("section", "")).strip().lower()
        text = str(sec.get("text", "")).strip()
        if sec.get("doc_url") and not source_url:
            source_url = str(sec.get("doc_url"))
        if sec.get("doc_title") and not source_title:
            source_title = str(sec.get("doc_title"))
        if sec.get("last_updated") and not last_updated:
            last_updated = str(sec.get("last_updated"))

        if name == "what it does" and text and not description:
            description = _one_sentence(text)
        elif name == "parameters" and text:
            for line in _extract_list_lines(text, limit=20):
                if ":" in line:
                    k, v = line.split(":", 1)
                    parameters.append({"name": k.strip(), "detail": v.strip()})
                else:
                    parameters.append({"name": line.strip(), "detail": ""})
        elif name == "returns" and text and not returns_text:
            returns_text = _one_sentence(text)

    if description:
        guidance["description"] = description
    if parameters:
        guidance["parameters"] = parameters
    if returns_text:
        guidance["returns_text"] = returns_text
    guidance["source"] = {
        "url": source_url or None,
        "title": source_title or None,
        "last_updated": last_updated or None,
    }
    return guidance


def _apply_structured_alternatives(guidance: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    if not guidance:
        return guidance
    raw = metadata.get("alternatives") if isinstance(metadata, dict) else None
    if not isinstance(raw, list) or not raw:
        return guidance
    out: list[dict[str, Any]] = []
    for alt in raw:
        if not isinstance(alt, dict):
            continue
        option = str(alt.get("option", "")).strip()
        reason = str(alt.get("reason", "")).strip()
        if not option or not reason:
            continue
        out.append(
            {
                "name": option,
                "why": reason,
                "doc_url": metadata.get("source_url"),
            }
        )
    if out:
        guidance["alternatives"] = out
    return guidance


def _one_sentence(text: str) -> str:
    clean = " ".join(text.replace("\n", " ").split())
    return clean[:300].strip()


def _build_guidance(query: str, hits: list) -> dict[str, Any]:
    if not hits:
        return {
            "command_or_function": None,
            "signature": None,
            "returns": None,
            "confidence": 0.0,
            "examples": [],
            "cautions": [],
            "citations": [],
            "alternatives": [],
            "show_top_matches": False,
            "preview": None,
        }

    # Choose a primary item so output remains focused on one function/command.
    item_scores: dict[str, float] = {}
    for hit in hits:
        item_scores[hit.item] = item_scores.get(hit.item, 0.0) + float(hit.score)
    primary_item = max(item_scores, key=item_scores.get)
    primary_hits = [hit for hit in hits if hit.item == primary_item]
    if not primary_hits:
        primary_hits = [hits[0]]
    primary_hits.sort(key=lambda h: h.score, reverse=True)
    preferred_sections = [
        "what it does",
        "use when",
        "signature",
        "parameters",
        "examples",
        "gotchas / version notes",
        "alternatives",
    ]
    top = primary_hits[0]
    for pref in preferred_sections:
        candidate = next((h for h in primary_hits if (h.section or "").lower() == pref), None)
        if candidate is not None:
            top = candidate
            break

    examples = []
    cautions = []
    citations = []
    alternatives = []
    seen_refs: set[str] = set()
    returns = None

    for hit in primary_hits:
        ref = hit.source_url or None
        if ref and ref not in seen_refs:
            seen_refs.add(ref)
            citations.append(
                {
                    "url": ref,
                    "title": hit.source_title or hit.item,
                    "section": hit.section,
                    "item": hit.item,
                }
            )
        section = (hit.section or "").lower()
        if section == "examples":
            cleaned = _strip_chunk_scaffold(hit.text)
            code_blocks = _extract_code_blocks(cleaned)
            if code_blocks:
                for lang, code in code_blocks:
                    examples.append(
                        {
                            "text": f"```{lang}\n{code}\n```" if lang else f"```\n{code}\n```",
                            "doc_url": hit.source_url,
                            "doc_title": hit.source_title or hit.item,
                            "confidence": hit.score,
                            "language": _normalize_language(lang),
                        }
                    )
            else:
                examples.append(
                    {
                        "text": cleaned,
                        "doc_url": hit.source_url,
                        "doc_title": hit.source_title or hit.item,
                        "confidence": hit.score,
                    }
                )
        if section in {"gotchas / version notes", "cautions", "warnings"}:
            cleaned = _strip_chunk_scaffold(hit.text)
            caution_lines = _extract_list_lines(cleaned, limit=20)
            if caution_lines:
                for line in caution_lines:
                    cautions.append(
                        {
                            "text": line,
                            "doc_url": hit.source_url,
                            "doc_title": hit.source_title or hit.item,
                            "confidence": hit.score,
                        }
                    )
            else:
                cautions.append(
                    {
                        "text": cleaned,
                        "doc_url": hit.source_url,
                        "doc_title": hit.source_title or hit.item,
                        "confidence": hit.score,
                    }
                )
        if section == "returns" and returns is None:
            returns = {
                "text": _strip_chunk_scaffold(hit.text),
                "doc_url": hit.source_url,
                "doc_title": hit.source_title or hit.item,
            }
        if section == "alternatives":
            for alt_line in _extract_list_lines(_strip_chunk_scaffold(hit.text), limit=12):
                alternatives.append(
                    {
                        "name": alt_line,
                        "why": "Alternative approach from official docs context.",
                        "doc_url": hit.source_url,
                    }
                )

    distinct_items = len({hit.item for hit in hits})
    show_top_matches = distinct_items > 1 or float(top.score) < 0.62
    if distinct_items > 1:
        item_best: dict[str, Any] = {}
        for hit in hits:
            current = item_best.get(hit.item)
            if current is None or float(hit.score) > float(current.score):
                item_best[hit.item] = hit
        for item_name, hit in sorted(item_best.items(), key=lambda pair: float(pair[1].score), reverse=True):
            if item_name == primary_item:
                continue
            alternatives.append(
                {
                    "name": item_name,
                    "why": f"Close match for this query (confidence {float(hit.score):.3f}).",
                    "doc_url": hit.source_url,
                    "confidence": float(hit.score),
                }
            )
    # de-dup alternatives while preserving order
    seen_alt: set[str] = set()
    dedup_alts: list[dict[str, Any]] = []
    for alt in alternatives:
        key = alt.get("name", "").strip().lower()
        if not key or key in seen_alt:
            continue
        seen_alt.add(key)
        dedup_alts.append(alt)

    return {
        "command_or_function": primary_item,
        "signature": top.signature,
        "returns": returns,
        "confidence": top.score,
        "examples": examples,
        "cautions": cautions,
        "citations": citations,
        "alternatives": dedup_alts,
        "show_top_matches": show_top_matches,
        "preview": {
            "item": top.item,
            "section": top.section,
            "text": _strip_chunk_scaffold(top.text),
            "doc_url": top.source_url,
            "confidence": top.score,
        },
    }


def _prefer_examples_by_language(guidance: dict[str, Any], preferred_language: str | None) -> dict[str, Any]:
    if not guidance:
        return guidance
    wanted = _normalize_language(preferred_language)
    if not wanted:
        return guidance
    examples = list(guidance.get("examples") or [])
    if not examples:
        return guidance

    compatible = {"javascript": {"jsx"}, "typescript": {"tsx"}, "bash": {"sh"}, "python": set()}
    accepted = {wanted} | compatible.get(wanted, set())

    def _example_lang(example: dict[str, Any]) -> str:
        direct = _normalize_language(str(example.get("language") or ""))
        if direct:
            return direct
        blocks = _extract_code_blocks(str(example.get("text") or ""))
        if blocks:
            return _normalize_language(blocks[0][0])
        return ""

    matched = [ex for ex in examples if _example_lang(ex) in accepted]
    others = [ex for ex in examples if ex not in matched]
    guidance["examples"] = matched + others
    guidance["preferred_language"] = wanted
    return guidance


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
    include_full_doc: bool = False,
    preferred_language: str | None = None,
    index_root: Path | None = None,
) -> dict[str, Any] | AskResponse:
    clean_query = query.strip()
    if not clean_query:
        raise ValueError("query must not be empty")
    base_dir = index_root.expanduser().resolve() if index_root else INDEX_ROOT

    parsed_library, parsed_version, stripped_query = split_inline_library_version(clean_query)
    requested_version = version
    autodetected = False
    warnings: list[str] = []

    if library is None and parsed_library:
        library = parsed_library
        version = version or parsed_version
        requested_version = version
        clean_query = stripped_query
        if not clean_query:
            raise ValueError("query content is empty after parsing library@version prefix")

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

    resolved_version, version_resolution_reason = resolve_version_with_reason(
        library,
        version,
        index_root=base_dir,
        allow_remote=(policy != "offline-only"),
    )
    index_dir = ensure_index_exists(
        library,
        resolved_version,
        index_root=base_dir,
        ensure_fresh=ensure_fresh,
        strict_fresh=strict_fresh_effective,
    )

    effective_version = index_dir.name
    retriever = Retriever.get(index_dir=index_dir)
    query_intent = infer_query_intent(clean_query)
    hits = retriever.search(clean_query, top_k=top_k, intent=query_intent)
    freshness = freshness_status()

    if not freshness.get("fresh", False):
        warnings.append("Index freshness check failed or is stale. Run `tref update`.")
    if freshness.get("verified") is False:
        warnings.append("Index checksum verification is missing/failed for current local snapshot.")
    if freshness.get("require_signature") and (freshness.get("verified_signature") is not True):
        warnings.append("Signature verification is required but missing/failed for current local snapshot.")
    if freshness.get("trusted") is False:
        warnings.append("Index snapshot is not fully trusted under current trust policy.")
    version_mismatch = bool(requested_version) and (effective_version != requested_version)
    if version_mismatch:
        if version_resolution_reason.startswith("compatible-"):
            warnings.append(
                f"Requested version '{requested_version}' mapped to compatible '{effective_version}' ({version_resolution_reason})."
            )
        else:
            warnings.append(f"Requested version '{requested_version}' not found; using '{effective_version}'.")

    provenance = {
        "index_dir": str(index_dir),
        "embedding_model": retriever.index_meta.get("embedding_model"),
        "kb_commit": retriever.index_meta.get("kb_commit"),
        "build_hash": retriever.index_meta.get("build_hash"),
        "builder_version": retriever.index_meta.get("builder_version"),
        "freshness_policy": policy,
        "query_intent": query_intent,
    }

    guidance = _build_guidance(clean_query, hits)
    sections: list[dict[str, Any]] = []
    top_item: str | None = None
    if hits:
        top_item = guidance.get("command_or_function") or hits[0].item
        sections = retriever.item_document(top_item)
        guidance = _augment_guidance_from_sections(guidance, sections)
        guidance = _extract_structured_fields_from_sections(guidance, sections)
        guidance = _apply_structured_alternatives(guidance, retriever.item_metadata(top_item))
    guidance = _prefer_examples_by_language(guidance, preferred_language)
    full_document = None
    query_flags = _query_flags(clean_query)
    if hits and (include_full_doc or query_flags["overview_focus"]):
        if not top_item:
            top_item = guidance.get("command_or_function") or hits[0].item
        if not sections:
            sections = retriever.item_document(top_item)
        full_document = {
            "item": top_item,
            "sections": sections,
        }

    response = AskResponse(
        library=library,
        version=effective_version,
        version_requested=requested_version,
        version_resolution={
            "requested": requested_version,
            "resolved": effective_version,
            "reason": version_resolution_reason,
        },
        version_mismatch=version_mismatch,
        query=clean_query,
        results=hits,
        autodetected_library=autodetected,
        freshness=freshness,
        provenance=provenance,
        guidance=guidance,
        warnings=warnings,
        full_document=full_document,
    )

    if llm:
        response.answer = _ollama_answer(clean_query, [r.to_dict() for r in hits], llm_model)

    if json_mode:
        return response.to_dict()
    return response
