from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx

from tref.config import (
    COSIGN_BIN,
    COSIGN_KEY_PATH,
    HTTP_MAX_RETRIES,
    HTTP_RETRY_BACKOFF_SECONDS,
    HTTP_TIMEOUT_SECONDS,
    INDEX_ROOT,
    MAX_DOWNLOAD_BYTES,
    MAX_INDEX_AGE_DAYS,
    REQUIRE_SIGNATURE,
    UPDATE_STATE_CACHE,
    UPDATE_STRICT_VERIFY,
    ensure_dirs,
    get_release_asset_name,
    get_release_checksum_asset_name,
    get_release_signature_asset_name,
    get_releases_api_url,
)
from tref.errors import FreshnessError, UpdateError


def _http_get_json(url: str) -> dict:
    last_error: Exception | None = None
    for attempt in range(HTTP_MAX_RETRIES):
        try:
            response = httpx.get(
                url,
                timeout=HTTP_TIMEOUT_SECONDS,
                headers={"User-Agent": "tref/0.3.0"},
                follow_redirects=True,
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
            if attempt < (HTTP_MAX_RETRIES - 1):
                time.sleep(HTTP_RETRY_BACKOFF_SECONDS * (2**attempt))
    raise UpdateError("UPDATE_HTTP_ERROR", f"Failed GET {url}: {last_error}")


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
                raise UpdateError("UPDATE_UNSAFE_ARCHIVE", f"Unsafe archive entry blocked: {member.name}")
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
        return {
            "fresh": False,
            "reason": "never_updated",
            "verified": False,
            "verified_signature": False,
            "strict_verify": False,
            "require_signature": REQUIRE_SIGNATURE,
            "trusted": False,
            "sla_met": False,
            "max_age_days": max_age_days,
        }
    try:
        fetched_dt = datetime.fromisoformat(fetched_at)
    except ValueError:
        return {
            "fresh": False,
            "reason": "invalid_state_timestamp",
            "verified": False,
            "verified_signature": False,
            "strict_verify": False,
            "require_signature": REQUIRE_SIGNATURE,
            "trusted": False,
            "sla_met": False,
            "max_age_days": max_age_days,
        }
    if fetched_dt.tzinfo is None:
        fetched_dt = fetched_dt.replace(tzinfo=UTC)
    now = datetime.now(tz=UTC)
    age = now - fetched_dt
    expires_at = fetched_dt + timedelta(days=max_age_days)
    days_remaining = round((expires_at - now).total_seconds() / 86400.0, 2)
    status = {
        "fresh": age <= timedelta(days=max_age_days),
        "age_days": round(age.total_seconds() / 86400.0, 2),
        "fetched_at": fetched_dt.isoformat(),
        "expires_at": expires_at.isoformat(),
        "days_remaining": days_remaining,
        "release_tag": state.get("release_tag"),
        "verified": bool(state.get("verified", False)),
        "verified_signature": bool(state.get("verified_signature", False)),
        "strict_verify": bool(state.get("strict_verify", False)),
        "require_signature": bool(state.get("require_signature", False)),
        "max_age_days": max_age_days,
    }
    status["trusted"] = bool(status["verified"]) and (
        (not status["require_signature"]) or bool(status["verified_signature"])
    )
    status["sla_met"] = bool(status["fresh"])
    return status


def _download_file(url: str, target_path: Path) -> int:
    total = 0
    with httpx.stream(
        "GET",
        url,
        timeout=max(HTTP_TIMEOUT_SECONDS, 60.0),
        headers={"User-Agent": "tref/0.3.0"},
        follow_redirects=True,
    ) as stream:
        stream.raise_for_status()
        with target_path.open("wb") as fh:
            for chunk in stream.iter_bytes():
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    raise UpdateError("UPDATE_DOWNLOAD_TOO_LARGE", f"Download exceeded safety limit: {MAX_DOWNLOAD_BYTES} bytes")
                fh.write(chunk)
    return total


def _read_checksum_file(path: Path) -> str:
    content = path.read_text(encoding="utf-8").strip().splitlines()
    if not content:
        raise UpdateError("UPDATE_CHECKSUM_EMPTY", "Empty checksum file")
    return content[0].split()[0].strip().lower()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _verify_signature_with_cosign(archive_path: Path, signature_path: Path) -> bool:
    if not COSIGN_KEY_PATH:
        return False
    cmd = [
        COSIGN_BIN,
        "verify-blob",
        "--key",
        COSIGN_KEY_PATH,
        "--signature",
        str(signature_path),
        str(archive_path),
    ]
    try:
        completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except Exception:
        return False
    return completed.returncode == 0


def _discover_stage_root(stage_dir: Path) -> Path:
    if (stage_dir / "_manifest.json").exists():
        return stage_dir
    for child in stage_dir.iterdir():
        if child.is_dir() and (child / "_manifest.json").exists():
            return child
    raise UpdateError("UPDATE_INVALID_ARCHIVE", "Extracted archive does not contain _manifest.json")


def _atomic_replace_index_tree(stage_root: Path) -> None:
    ensure_dirs()
    backup_root = INDEX_ROOT.parent / f"{INDEX_ROOT.name}.backup"
    temp_new_root = INDEX_ROOT.parent / f"{INDEX_ROOT.name}.new"

    shutil.rmtree(temp_new_root, ignore_errors=True)
    shutil.copytree(stage_root, temp_new_root)

    # Backup current indexes for rollback.
    if INDEX_ROOT.exists():
        shutil.rmtree(backup_root, ignore_errors=True)
        INDEX_ROOT.replace(backup_root)

    try:
        temp_new_root.replace(INDEX_ROOT)
    except Exception as exc:
        if backup_root.exists() and not INDEX_ROOT.exists():
            backup_root.replace(INDEX_ROOT)
        raise UpdateError("UPDATE_ATOMIC_SWAP_FAILED", f"Atomic swap failed: {exc}") from exc
    finally:
        shutil.rmtree(backup_root, ignore_errors=True)
        shutil.rmtree(temp_new_root, ignore_errors=True)


def update_indexes(silent: bool = False, strict_verify: bool = UPDATE_STRICT_VERIFY) -> Path:
    ensure_dirs()
    releases_api = get_releases_api_url()
    release = _http_get_json(releases_api)

    archive_name = get_release_asset_name()
    checksum_name = get_release_checksum_asset_name()
    signature_name = get_release_signature_asset_name()

    asset_url = _find_asset_url(release, archive_name)
    if not asset_url:
        raise UpdateError("UPDATE_ASSET_NOT_FOUND", f"Release asset '{archive_name}' not found")

    checksum_url = _find_asset_url(release, checksum_name)
    signature_url = _find_asset_url(release, signature_name)

    if strict_verify and not checksum_url:
        raise UpdateError(
            "UPDATE_CHECKSUM_MISSING",
            f"Strict verification enabled but checksum asset '{checksum_name}' was not found",
        )
    if REQUIRE_SIGNATURE and not signature_url:
        raise UpdateError(
            "UPDATE_SIGNATURE_MISSING",
            f"Signature is required but asset '{signature_name}' was not found",
        )

    archive_path = INDEX_ROOT.parent / archive_name
    archive_tmp = archive_path.with_suffix(archive_path.suffix + ".tmp")
    _download_file(asset_url, archive_tmp)
    archive_tmp.replace(archive_path)

    verified = False
    verified_signature = False
    expected_sha = None
    actual_sha = _sha256_file(archive_path)

    if checksum_url:
        checksum_path = INDEX_ROOT.parent / checksum_name
        checksum_tmp = checksum_path.with_suffix(checksum_path.suffix + ".tmp")
        _download_file(checksum_url, checksum_tmp)
        checksum_tmp.replace(checksum_path)
        expected_sha = _read_checksum_file(checksum_path)
        verified = (actual_sha == expected_sha)
        checksum_path.unlink(missing_ok=True)
    elif strict_verify:
        raise UpdateError("UPDATE_CHECKSUM_REQUIRED", "Strict verification requires checksum file")

    if signature_url:
        signature_path = INDEX_ROOT.parent / signature_name
        signature_tmp = signature_path.with_suffix(signature_path.suffix + ".tmp")
        _download_file(signature_url, signature_tmp)
        signature_tmp.replace(signature_path)
        verified_signature = _verify_signature_with_cosign(archive_path, signature_path)
        signature_path.unlink(missing_ok=True)

    if strict_verify and not verified:
        archive_path.unlink(missing_ok=True)
        raise UpdateError("UPDATE_CHECKSUM_MISMATCH", "Archive checksum verification failed")

    if strict_verify and COSIGN_KEY_PATH and not verified_signature:
        archive_path.unlink(missing_ok=True)
        raise UpdateError("UPDATE_SIGNATURE_FAILED", "Archive signature verification failed")
    if REQUIRE_SIGNATURE and not verified_signature:
        archive_path.unlink(missing_ok=True)
        raise UpdateError("UPDATE_SIGNATURE_REQUIRED", "Signature verification is required but failed/missing")

    stage_dir = INDEX_ROOT.parent / ".tref-index-stage"
    shutil.rmtree(stage_dir, ignore_errors=True)
    stage_dir.mkdir(parents=True, exist_ok=True)

    try:
        _safe_extract_tar(archive_path, stage_dir)
        stage_root = _discover_stage_root(stage_dir)
        _atomic_replace_index_tree(stage_root)
    finally:
        shutil.rmtree(stage_dir, ignore_errors=True)
        archive_path.unlink(missing_ok=True)

    _write_update_state(
        {
            "fetched_at": datetime.now(tz=UTC).isoformat(),
            "release_tag": release.get("tag_name"),
            "release_asset_name": archive_name,
            "release_asset_url": asset_url,
            "release_published_at": release.get("published_at"),
            "verified": verified,
            "verified_signature": verified_signature,
            "sha256": actual_sha,
            "expected_sha256": expected_sha,
            "strict_verify": strict_verify,
            "require_signature": REQUIRE_SIGNATURE,
            "releases_api": releases_api,
        }
    )

    if not silent:
        print(
            f"Updated indexes in {INDEX_ROOT} "
            f"(verified={verified}, signature={verified_signature}, require_signature={REQUIRE_SIGNATURE})"
        )
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
        untrusted = not status.get("trusted", False)
        if (not status.get("fresh", False)) or (UPDATE_STRICT_VERIFY and untrusted):
            try:
                update_indexes(silent=True, strict_verify=UPDATE_STRICT_VERIFY)
            except Exception:
                if strict_fresh:
                    raise FreshnessError(
                        "FRESHNESS_STALE",
                        f"Indexes are stale/unverified ({status}). Update failed in strict mode.",
                    ) from None

    if candidate.exists():
        return candidate

    if ensure_fresh and index_root == INDEX_ROOT:
        try:
            update_indexes(silent=True, strict_verify=UPDATE_STRICT_VERIFY)
        except Exception:
            pass

    fallback = index_root / library / "latest"
    if candidate.exists():
        return candidate
    if version != "latest" and fallback.exists():
        return fallback

    raise FreshnessError(
        "INDEX_NOT_FOUND",
        f"No local index for {library}@{version}. Run 'tref update' or build a custom index.",
    )
