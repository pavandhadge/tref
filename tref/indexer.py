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
}

REQUIRED_HEADINGS = {"Signature", "Parameters", "Examples", "Gotchas / Version Notes"}


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


def _validate_frontmatter(meta: dict[str, Any], doc_path: Path) -> None:
    missing = REQUIRED_FRONTMATTER_KEYS.difference(meta.keys())
    if missing:
        raise ValidationError("KB_FRONTMATTER_MISSING", f"Missing frontmatter keys in {doc_path}: {sorted(missing)}")

    if not isinstance(meta.get("keywords"), list) or not all(isinstance(x, str) for x in meta["keywords"]):
        raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid keywords in {doc_path}; expected list[str]")

    for key in ["library", "version", "category", "item", "type", "signature", "last_updated"]:
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise ValidationError("KB_FRONTMATTER_INVALID", f"Invalid '{key}' in {doc_path}")


def _validate_sections(sections: list[tuple[str, str]], doc_path: Path) -> None:
    seen = {title for title, _ in sections}
    missing = REQUIRED_HEADINGS.difference(seen)
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
        chunk_text = (
            f"# {meta['library']}.{meta['item']}\n"
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
                "signature": str(meta["signature"]),
                "keywords": list(meta["keywords"]),
                "section": section_title,
                "source_last_updated": str(meta["last_updated"]),
                "source_doc_hash": doc_hash,
            }
        )
    return chunks


def _build_faiss_index(
    chunks: list[dict[str, Any]],
    output_dir: Path,
    model_name: str = EMBED_MODEL,
    kb_commit: str = "unknown",
) -> dict[str, Any]:
    if not chunks:
        raise ValidationError("INDEX_EMPTY", "No chunks found to index")

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
