from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import faiss
import frontmatter
import numpy as np
from fastembed import TextEmbedding

from tref.config import EMBED_MODEL
from tref.errors import ValidationError

REQUIRED_FRONTMATTER_KEYS = {
    "library",
    "version",
    "category",
    "item",
    "type",
    "signature",
    "keywords",
    "last_updated",
    "schema_version",
    "intent",
    "source_url",
    "source_title",
}

SCHEMA_V2_REQUIRED_HEADINGS = {
    "Signature",
    "What It Does",
    "Use When",
    "Examples",
    "Alternatives",
    "Gotchas / Version Notes",
    "References",
}


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _split_sections(content: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            body = "\n".join(current_lines).strip()
            if body:
                sections.append((current_title, body))
            current_title = line.removeprefix("## ").strip()
            current_lines = []
        else:
            current_lines.append(line)

    body = "\n".join(current_lines).strip()
    if body:
        sections.append((current_title, body))

    return sections


def _normalized_item_heading(library: str, item: str) -> str:
    prefix = f"{library}."
    if item.startswith(prefix):
        return item
    return f"{library}.{item}"


def _validate_frontmatter(meta: dict[str, Any], doc_path: Path) -> None:
    missing = REQUIRED_FRONTMATTER_KEYS.difference(meta.keys())
    if missing:
        raise ValidationError("KB_FRONTMATTER_MISSING", f"Missing frontmatter keys in {doc_path}: {sorted(missing)}")

    if not isinstance(meta.get("keywords"), list) or not all(isinstance(x, str) for x in meta["keywords"]):
        raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid keywords in {doc_path}; expected list[str]")
    if not isinstance(meta.get("schema_version"), str) or str(meta["schema_version"]).strip() != "2.0":
        raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid 'schema_version' in {doc_path}; expected '2.0'")
    if not isinstance(meta.get("intent"), str) or not str(meta["intent"]).strip():
        raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid 'intent' in {doc_path}; expected short string")

    for key in ["library", "version", "category", "item", "type", "signature", "last_updated"]:
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid '{key}' in {doc_path}")
    if not isinstance(meta.get("source_url"), str) or not meta["source_url"].startswith(("http://", "https://")):
        raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid 'source_url' in {doc_path}")
    if not isinstance(meta.get("source_title"), str) or not meta["source_title"].strip():
        raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid 'source_title' in {doc_path}")
    if "aliases" in meta and (
        not isinstance(meta["aliases"], list) or not all(isinstance(x, str) and x.strip() for x in meta["aliases"])
    ):
        raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid 'aliases' in {doc_path}; expected list[str]")


def _validate_sections(sections: list[tuple[str, str]], doc_path: Path) -> None:
    seen = {title for title, _ in sections}
    missing = SCHEMA_V2_REQUIRED_HEADINGS.difference(seen)
    if missing:
        raise ValidationError("KB_SECTION_MISSING", f"Missing required headings in {doc_path}: {sorted(missing)}")


def _parse_markdown(doc_path: Path, kb_root: Path) -> list[dict[str, Any]]:
    post = frontmatter.load(doc_path)
    meta = dict(post.metadata)
    _validate_frontmatter(meta, doc_path)

    sections = _split_sections(post.content)
    _validate_sections(sections, doc_path)

    chunks: list[dict[str, Any]] = []
    rel = doc_path.relative_to(kb_root).as_posix()
    doc_hash = _sha256_text(post.content)

    for idx, (section_title, section_body) in enumerate(sections):
        if section_title == "Overview" and section_body.strip().startswith("# "):
            # Skip title-only preamble chunks; they reduce ranking quality.
            continue
        chunk_text = (
            f"# {_normalized_item_heading(str(meta['library']), str(meta['item']))}\n"
            f"## {section_title}\n"
            f"{section_body}"
        ).strip()
        chunks.append(
            {
                "id": f"{meta['library']}::{meta['version']}::{meta['item']}::{idx}",
                "text": chunk_text,
                "citation": rel,
                "library": str(meta["library"]),
                "version": str(meta["version"]),
                "item": str(meta["item"]),
                "type": str(meta["type"]),
                "signature": str(meta["signature"]),
                "keywords": list(meta["keywords"]),
                "aliases": list(meta.get("aliases", [])),
                "intent": str(meta.get("intent", "")),
                "section": section_title,
                "source_last_updated": str(meta["last_updated"]),
                "source_doc_hash": doc_hash,
                "source_url": str(meta.get("source_url", "")).strip() or None,
                "source_title": str(meta.get("source_title", "")).strip() or None,
            }
        )
    return chunks


def _build_faiss_index(
    chunks: list[dict[str, Any]],
    output_dir: Path,
    model_name: str = EMBED_MODEL,
    kb_commit: str = "unknown",
    embedder: TextEmbedding | None = None,
) -> dict[str, Any]:
    if not chunks:
        raise ValidationError("INDEX_EMPTY", "No chunks found to index")

    if embedder is None:
        embedder = TextEmbedding(model_name=model_name)
    vectors = list(embedder.embed([chunk["text"] for chunk in chunks]))
    matrix = np.array(vectors, dtype="float32")
    faiss.normalize_L2(matrix)

    index = faiss.IndexFlatIP(matrix.shape[1])
    index.add(matrix)

    output_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output_dir / "index.faiss"))

    with (output_dir / "chunks.jsonl").open("w", encoding="utf-8") as fh:
        for chunk in chunks:
            fh.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    joined_ids = "\n".join(chunk["id"] + "|" + chunk["source_doc_hash"] for chunk in chunks)
    build_hash = _sha256_text(joined_ids)

    now = datetime.now(tz=UTC)
    source_date_epoch = os.getenv("SOURCE_DATE_EPOCH")
    built_on = now.isoformat()
    if source_date_epoch:
        try:
            built_on = datetime.fromtimestamp(int(source_date_epoch), tz=UTC).isoformat()
        except Exception:
            pass

    meta = {
        "embedding_model": model_name,
        "dimension": int(matrix.shape[1]),
        "count": int(matrix.shape[0]),
        "built_on": built_on,
        "kb_commit": kb_commit,
        "build_hash": build_hash,
        "builder_version": "tref-0.3.0",
    }
    (output_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def _detect_kb_commit(kb_root: Path) -> str:
    env_commit = os.getenv("TREF_KB_COMMIT")
    if env_commit:
        return env_commit
    head = kb_root / ".git" / "HEAD"
    if head.exists():
        return "git-local"
    return "unknown"


def build_indexes(kb_root: Path, output_root: Path) -> dict[str, Any]:
    kb_root = kb_root.expanduser().resolve()
    output_root = output_root.expanduser().resolve()

    kb_commit = _detect_kb_commit(kb_root)
    embedder = TextEmbedding(model_name=EMBED_MODEL)
    summary: dict[str, Any] = {
        "libraries": {},
        "built_on": datetime.now(tz=UTC).isoformat(),
        "kb_commit": kb_commit,
        "builder_version": "tref-0.3.0",
    }

    for library_dir in sorted(p for p in kb_root.iterdir() if p.is_dir()):
        library = library_dir.name
        versions: list[str] = []
        latest_from_manifest: str | None = None

        for version_dir in sorted(p for p in library_dir.iterdir() if p.is_dir()):
            version = version_dir.name
            doc_paths = sorted(version_dir.rglob("*.md"))
            if not doc_paths:
                continue
            chunks: list[dict[str, Any]] = []
            for doc_path in doc_paths:
                chunks.extend(_parse_markdown(doc_path, kb_root=kb_root))

            meta = _build_faiss_index(
                chunks,
                output_root / library / version,
                kb_commit=kb_commit,
                embedder=embedder,
            )
            versions.append(version)
            if version == "latest":
                latest_from_manifest = "latest"
            summary["libraries"].setdefault(library, {})[version] = {
                "count": meta["count"],
                "build_hash": meta["build_hash"],
            }

        if versions:
            latest = latest_from_manifest or sorted(v for v in versions if v != "latest")[-1]
            summary["libraries"][library]["versions"] = versions
            summary["libraries"][library]["latest"] = latest

    (output_root / "_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def validate_kb(kb_root: Path) -> dict[str, Any]:
    kb_root = kb_root.expanduser().resolve()
    total_docs = 0
    errors: list[str] = []
    for doc_path in sorted(kb_root.rglob("*.md")):
        try:
            _parse_markdown(doc_path, kb_root=kb_root)
            total_docs += 1
        except Exception as exc:
            errors.append(f"{doc_path}: {exc}")
    return {"valid": len(errors) == 0, "docs": total_docs, "errors": errors}
