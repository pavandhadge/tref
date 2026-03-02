from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

import httpx

from tref.config import (
    HTTP_MAX_RETRIES,
    HTTP_RETRY_BACKOFF_SECONDS,
    HTTP_TIMEOUT_SECONDS,
    INDEX_ROOT,
    MANIFEST_CACHE,
    get_kb_manifest_url,
    ensure_dirs,
)

LIBVER_RE = re.compile(r"^(?P<library>[a-zA-Z0-9_.-]+)@(?P<version>[a-zA-Z0-9_.-]+)$")
WORD_RE = re.compile(r"[a-zA-Z0-9_.-]+")

LIBRARY_HINTS: dict[str, tuple[str, ...]] = {
    "pandas": ("dataframe", "series", "groupby", "merge", "pivot", "read_csv", "pd"),
    "polars": ("lazyframe", "group_by", "pl", "scan_parquet", "collect"),
    "git": ("commit", "rebase", "cherry-pick", "checkout", "stash", "branch", "merge"),
    "docker": ("container", "image", "dockerfile", "compose", "volume", "port", "run"),
}


def parse_library_version(token: str) -> tuple[str | None, str | None]:
    match = LIBVER_RE.match(token.strip())
    if not match:
        return None, None
    return match.group("library"), match.group("version")


def split_inline_library_version(query: str) -> tuple[str | None, str | None, str]:
    parts = query.strip().split()
    if not parts:
        return None, None, ""
    lib, ver = parse_library_version(parts[0])
    if not lib:
        return None, None, query.strip()
    return lib, ver, " ".join(parts[1:]).strip()


def load_manifest(refresh: bool = False) -> dict[str, Any]:
    ensure_dirs()
    if MANIFEST_CACHE.exists() and not refresh:
        return json.loads(MANIFEST_CACHE.read_text(encoding="utf-8"))
    last_error: Exception | None = None
    url = get_kb_manifest_url()
    for attempt in range(HTTP_MAX_RETRIES):
        try:
            response = httpx.get(
                url,
                timeout=HTTP_TIMEOUT_SECONDS,
                headers={"User-Agent": "tref/0.2.0"},
                follow_redirects=True,
            )
            response.raise_for_status()
            data = response.json()
            tmp = MANIFEST_CACHE.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            tmp.replace(MANIFEST_CACHE)
            return data
        except Exception as exc:
            last_error = exc
            if attempt < (HTTP_MAX_RETRIES - 1):
                time.sleep(HTTP_RETRY_BACKOFF_SECONDS * (2**attempt))
    if MANIFEST_CACHE.exists():
        return json.loads(MANIFEST_CACHE.read_text(encoding="utf-8"))
    if last_error:
        return {"libraries": {}, "error": str(last_error)}
    return {"libraries": {}}


def local_versions(library: str, index_root: Path = INDEX_ROOT) -> list[str]:
    library_dir = index_root / library
    if not library_dir.exists():
        return []
    versions = [p.name for p in library_dir.iterdir() if p.is_dir()]
    return sorted(versions)


def available_libraries(index_root: Path = INDEX_ROOT) -> list[str]:
    ensure_dirs()
    local = [p.name for p in index_root.iterdir() if p.is_dir()]
    manifest = load_manifest(refresh=False)
    remote = list(manifest.get("libraries", {}).keys())
    return sorted(set(local + remote))


def detect_library_from_query(query: str, index_root: Path = INDEX_ROOT) -> str | None:
    query_lower = query.lower()
    tokens = set(WORD_RE.findall(query_lower))
    scores: dict[str, int] = {}

    for library in available_libraries(index_root=index_root):
        score = 0
        if re.search(rf"\b{re.escape(library.lower())}\b", query_lower):
            score += 10

        for hint in LIBRARY_HINTS.get(library.lower(), ()):
            if hint in query_lower or hint in tokens:
                score += 2
        scores[library] = score

    if not scores:
        return None

    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_lib, top_score = ordered[0]
    if top_score <= 0:
        return None
    if len(ordered) > 1 and (top_score - ordered[1][1]) < 2:
        return None
    return top_lib


def resolve_version(library: str, requested: str | None, index_root: Path = INDEX_ROOT) -> str:
    versions = local_versions(library, index_root=index_root)
    manifest = load_manifest(refresh=False)
    manifest_info = manifest.get("libraries", {}).get(library, {})
    manifest_versions = manifest_info.get("versions", [])

    if requested:
        if requested in versions or requested in manifest_versions:
            return requested
        all_versions = sorted(set(versions + manifest_versions))
        for ver in all_versions:
            if ver.startswith(requested):
                return ver
        return requested

    if versions:
        if "latest" in versions:
            return "latest"
        return versions[-1]

    latest = manifest_info.get("latest")
    return latest if latest else "latest"
