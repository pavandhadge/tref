from __future__ import annotations

import hashlib
import json
import os
import tarfile
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx

from tref.config import (
    HTTP_MAX_RETRIES,
    HTTP_RETRY_BACKOFF_SECONDS,
    HTTP_TIMEOUT_SECONDS,
    INDEX_ROOT,
    MAX_DOWNLOAD_BYTES,
    MAX_INDEX_AGE_DAYS,
    UPDATE_STATE_CACHE,
    UPDATE_STRICT_VERIFY,
    ensure_dirs,
    get_release_asset_name,
    get_release_checksum_asset_name,
    get_releases_api_url,
)


def _http_get_json(url: str) -> dict:
    last_error: Exception | None = None
    for attempt in range(HTTP_MAX_RETRIES):
        try:
            response = httpx.get(
                url,
                timeout=HTTP_TIMEOUT_SECONDS,
                headers={"User-Agent": "tref/0.2.0"},
                follow_redirects=True,
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
            if attempt < (HTTP_MAX_RETRIES - 1):
                time.sleep(HTTP_RETRY_BACKOFF_SECONDS * (2**attempt))
    raise RuntimeError(f"Failed GET {url}: {last_error}") from last_error


def _find_asset_url(release_payload: dict, asset_name: str) -> str | None:
    assets = release_payload.get("assets", [])
    for asset in assets:
        if asset.get("name") == asset_name:
            url = asset.get("browser_download_url")
            if url:
                return str(url)
    return None


def _safe_extract_tar(archive_path: Path, target_dir: Path) -> None:
    with tarfile.open(archive_path, "r:gz") as tf:
        target_real = target_dir.resolve()
        for member in tf.getmembers():
            member_path = (target_dir / member.name).resolve()
            if os.path.commonpath([str(target_real), str(member_path)]) != str(target_real):
                raise RuntimeError(f"Unsafe archive entry blocked: {member.name}")
        tf.extractall(target_dir)


def _read_update_state() -> dict:
    if not UPDATE_STATE_CACHE.exists():
        return {}
    return json.loads(UPDATE_STATE_CACHE.read_text(encoding="utf-8"))


def _write_update_state(state: dict) -> None:
    tmp = UPDATE_STATE_CACHE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(UPDATE_STATE_CACHE)


def freshness_status(max_age_days: int = MAX_INDEX_AGE_DAYS) -> dict:
    state = _read_update_state()
    fetched_at = state.get("fetched_at")
    if not fetched_at:
        return {"fresh": False, "reason": "never_updated", "verified": False, "max_age_days": max_age_days}
    try:
        fetched_dt = datetime.fromisoformat(fetched_at)
    except ValueError:
        return {
            "fresh": False,
            "reason": "invalid_state_timestamp",
            "verified": False,
            "max_age_days": max_age_days,
        }
    if fetched_dt.tzinfo is None:
        fetched_dt = fetched_dt.replace(tzinfo=UTC)
    now = datetime.now(tz=UTC)
    age = now - fetched_dt
    return {
        "fresh": age <= timedelta(days=max_age_days),
        "age_days": round(age.total_seconds() / 86400.0, 2),
        "fetched_at": fetched_dt.isoformat(),
        "release_tag": state.get("release_tag"),
        "verified": bool(state.get("verified", False)),
        "max_age_days": max_age_days,
    }


def _download_file(url: str, target_path: Path) -> int:
    total = 0
    with httpx.stream(
        "GET",
        url,
        timeout=max(HTTP_TIMEOUT_SECONDS, 60.0),
        headers={"User-Agent": "tref/0.2.0"},
        follow_redirects=True,
    ) as stream:
        stream.raise_for_status()
        with target_path.open("wb") as fh:
            for chunk in stream.iter_bytes():
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    raise RuntimeError(f"Download exceeded safety limit: {MAX_DOWNLOAD_BYTES} bytes")
                fh.write(chunk)
    return total


def _read_checksum_file(path: Path) -> str:
    content = path.read_text(encoding="utf-8").strip().splitlines()
    if not content:
        raise RuntimeError("Empty checksum file")
    # supports either '<hash>' or '<hash>  <filename>'
    return content[0].split()[0].strip().lower()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def update_indexes(silent: bool = False, strict_verify: bool = UPDATE_STRICT_VERIFY) -> Path:
    ensure_dirs()
    releases_api = get_releases_api_url()
    release = _http_get_json(releases_api)

    archive_name = get_release_asset_name()
    checksum_name = get_release_checksum_asset_name()

    asset_url = _find_asset_url(release, archive_name)
    if not asset_url:
        raise RuntimeError(f"Release asset '{archive_name}' not found")

    checksum_url = _find_asset_url(release, checksum_name)
    if strict_verify and not checksum_url:
        raise RuntimeError(
            f"Strict verification enabled but checksum asset '{checksum_name}' was not found"
        )

    archive_path = INDEX_ROOT / archive_name
    archive_tmp = archive_path.with_suffix(archive_path.suffix + ".tmp")
    _download_file(asset_url, archive_tmp)
    archive_tmp.replace(archive_path)

    verified = False
    expected_sha = None
    actual_sha = _sha256_file(archive_path)

    if checksum_url:
        checksum_path = INDEX_ROOT / checksum_name
        checksum_tmp = checksum_path.with_suffix(checksum_path.suffix + ".tmp")
        _download_file(checksum_url, checksum_tmp)
        checksum_tmp.replace(checksum_path)
        expected_sha = _read_checksum_file(checksum_path)
        verified = (actual_sha == expected_sha)
        checksum_path.unlink(missing_ok=True)
    elif strict_verify:
        raise RuntimeError("Strict verification requires checksum file")

    if strict_verify and not verified:
        archive_path.unlink(missing_ok=True)
        raise RuntimeError("Archive checksum verification failed")

    _safe_extract_tar(archive_path, INDEX_ROOT)
    _write_update_state(
        {
            "fetched_at": datetime.now(tz=UTC).isoformat(),
            "release_tag": release.get("tag_name"),
            "release_asset_name": archive_name,
            "release_asset_url": asset_url,
            "release_published_at": release.get("published_at"),
            "verified": verified,
            "sha256": actual_sha,
            "expected_sha256": expected_sha,
            "strict_verify": strict_verify,
            "releases_api": releases_api,
        }
    )

    archive_path.unlink(missing_ok=True)

    if not silent:
        print(f"Updated indexes in {INDEX_ROOT} (verified={verified})")
    return INDEX_ROOT


def ensure_index_exists(
    library: str,
    version: str,
    index_root: Path = INDEX_ROOT,
    ensure_fresh: bool = True,
    strict_fresh: bool = False,
) -> Path:
    candidate = index_root / library / version
    if ensure_fresh and index_root == INDEX_ROOT:
        status = freshness_status()
        if (not status.get("fresh", False)) or (UPDATE_STRICT_VERIFY and not status.get("verified", False)):
            try:
                update_indexes(silent=True, strict_verify=UPDATE_STRICT_VERIFY)
            except Exception:
                if strict_fresh:
                    raise RuntimeError(
                        f"Indexes are stale/unverified ({status}). Update failed in strict mode."
                    ) from None

    if candidate.exists():
        return candidate

    if index_root == INDEX_ROOT:
        try:
            update_indexes(silent=True, strict_verify=UPDATE_STRICT_VERIFY)
        except Exception:
            pass

    fallback = index_root / library / "latest"
    if candidate.exists():
        return candidate
    if version != "latest" and fallback.exists():
        return fallback

    raise FileNotFoundError(
        f"No local index for {library}@{version}. Run 'tref update' or build a custom index."
    )
