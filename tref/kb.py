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
_MANIFEST_MEM_CACHE: dict[str, Any] | None = None

LIBRARY_HINTS: dict[str, tuple[str, ...]] = {
    "pandas": ("dataframe", "series", "groupby", "merge", "pivot", "read_csv", "pd"),
    "polars": ("lazyframe", "group_by", "pl", "scan_parquet", "collect"),
    "git": ("commit", "rebase", "cherry-pick", "checkout", "stash", "branch", "merge"),
    "docker": ("container", "image", "dockerfile", "compose", "volume", "port", "run"),
    "algorithms": ("binary search", "bubble sort", "sorting", "algorithm", "time complexity", "big o"),
    "react": ("react", "component", "hooks", "usestate", "state", "useeffect", "jsx"),
}


def _version_key(version: str) -> tuple:
    # Keep "latest" highest precedence for explicit local aliases.
    if version == "latest":
        return (1, 0)
    parts = re.split(r"[._-]", version)
    norm = []
    for part in parts:
        if part.isdigit():
            norm.append((0, int(part)))
        elif part:
            norm.append((1, part))
    return (0, tuple(norm))


def _normalized_version_text(version: str) -> str:
    v = version.strip()
    if v == "latest":
        return v
    parts = [p for p in re.split(r"[._-]", v) if p]
    while parts and parts[-1] == "0":
        parts.pop()
    return ".".join(parts) if parts else v


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
    global _MANIFEST_MEM_CACHE
    ensure_dirs()
    if _MANIFEST_MEM_CACHE is not None and not refresh:
        return _MANIFEST_MEM_CACHE
    if MANIFEST_CACHE.exists() and not refresh:
        _MANIFEST_MEM_CACHE = json.loads(MANIFEST_CACHE.read_text(encoding="utf-8"))
        return _MANIFEST_MEM_CACHE
    last_error: Exception | None = None
    url = get_kb_manifest_url()
    for attempt in range(HTTP_MAX_RETRIES):
        try:
            response = httpx.get(
                url,
                timeout=HTTP_TIMEOUT_SECONDS,
                headers={"User-Agent": "tref/0.3.0"},
                follow_redirects=True,
            )
            response.raise_for_status()
            data = response.json()
            tmp = MANIFEST_CACHE.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            tmp.replace(MANIFEST_CACHE)
            _MANIFEST_MEM_CACHE = data
            return data
        except Exception as exc:
            last_error = exc
            if attempt < (HTTP_MAX_RETRIES - 1):
                time.sleep(HTTP_RETRY_BACKOFF_SECONDS * (2**attempt))
    if MANIFEST_CACHE.exists():
        _MANIFEST_MEM_CACHE = json.loads(MANIFEST_CACHE.read_text(encoding="utf-8"))
        return _MANIFEST_MEM_CACHE
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


def detect_library_candidates(query: str, index_root: Path = INDEX_ROOT) -> list[dict[str, Any]]:
    query_lower = query.lower()
    tokens = set(WORD_RE.findall(query_lower))
    scored: list[dict[str, Any]] = []

    for library in available_libraries(index_root=index_root):
        score = 0
        reasons: list[str] = []
        if re.search(rf"\b{re.escape(library.lower())}\b", query_lower):
            score += 10
            reasons.append("library_name")

        for hint in LIBRARY_HINTS.get(library.lower(), ()):  # heuristic hints
            if hint in query_lower or hint in tokens:
                score += 2
                reasons.append(hint)

        scored.append({"library": library, "score": score, "reasons": reasons})

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored


def detect_library_from_query(
    query: str,
    index_root: Path = INDEX_ROOT,
    min_score: int = 2,
    min_margin: int = 2,
) -> tuple[str | None, list[dict[str, Any]]]:
    candidates = detect_library_candidates(query, index_root=index_root)
    if not candidates:
        return None, []

    top = candidates[0]
    second_score = candidates[1]["score"] if len(candidates) > 1 else -999

    if top["score"] < min_score:
        return None, candidates[:3]
    if (top["score"] - second_score) < min_margin:
        return None, candidates[:3]
    return top["library"], candidates[:3]


def resolve_version(
    library: str,
    requested: str | None,
    index_root: Path = INDEX_ROOT,
    allow_remote: bool = True,
) -> str:
    resolved, _reason = resolve_version_with_reason(
        library=library,
        requested=requested,
        index_root=index_root,
        allow_remote=allow_remote,
    )
    return resolved


def resolve_version_with_reason(
    library: str,
    requested: str | None,
    index_root: Path = INDEX_ROOT,
    allow_remote: bool = True,
) -> tuple[str, str]:
    versions = local_versions(library, index_root=index_root)
    manifest_info: dict[str, Any] = {}
    manifest_versions: list[str] = []
    if allow_remote:
        manifest = load_manifest(refresh=False)
        manifest_info = manifest.get("libraries", {}).get(library, {})
        manifest_versions = manifest_info.get("versions", [])

    all_versions = sorted(set(versions + manifest_versions), key=_version_key)

    if requested:
        if requested in versions or requested in manifest_versions:
            return requested, "exact"
        normalized_requested = _normalized_version_text(requested)
        for ver in all_versions:
            if _normalized_version_text(ver) == normalized_requested:
                return ver, "compatible-normalized"
        all_versions = sorted(set(versions + manifest_versions), key=_version_key)
        for ver in all_versions:
            if ver.startswith(requested):
                return ver, "compatible-prefix"
            if requested.startswith(ver):
                return ver, "compatible-prefix"
        return requested, "unresolved-requested"

    if versions:
        if "latest" in versions:
            return "latest", "default-latest-local"
        return sorted(versions, key=_version_key)[-1], "default-local-highest"

    latest = manifest_info.get("latest")
    return (latest if latest else "latest"), "default-remote-latest"
