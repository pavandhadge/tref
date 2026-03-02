from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import faiss
import frontmatter
import numpy as np
from fastembed import TextEmbedding

from tref.config import EMBED_MODEL

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


def _parse_markdown(doc_path: Path, kb_root: Path) -> list[dict[str, Any]]:
    post = frontmatter.load(doc_path)
    missing = REQUIRED_FRONTMATTER_KEYS.difference(post.metadata.keys())
    if missing:
        raise ValueError(f"Missing frontmatter keys in {doc_path}: {sorted(missing)}")

    meta = post.metadata
    sections = _split_sections(post.content)
    chunks: list[dict[str, Any]] = []
    rel = doc_path.relative_to(kb_root).as_posix()

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
            }
        )
    return chunks


def _build_faiss_index(chunks: list[dict[str, Any]], output_dir: Path, model_name: str = EMBED_MODEL) -> dict[str, Any]:
    if not chunks:
        raise ValueError("No chunks found to index")

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

    meta = {
        "embedding_model": model_name,
        "dimension": int(matrix.shape[1]),
        "count": int(matrix.shape[0]),
        "built_on": date.today().isoformat(),
    }
    (output_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def build_indexes(kb_root: Path, output_root: Path) -> dict[str, Any]:
    kb_root = kb_root.expanduser().resolve()
    output_root = output_root.expanduser().resolve()

    summary: dict[str, Any] = {"libraries": {}, "built_on": date.today().isoformat()}

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

            _build_faiss_index(chunks, output_root / library / version)
            versions.append(version)
            if version == "latest":
                latest_from_manifest = "latest"

        if versions:
            latest = latest_from_manifest or sorted(v for v in versions if v != "latest")[-1]
            summary["libraries"][library] = {
                "versions": versions,
                "latest": latest,
            }

    (output_root / "_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
