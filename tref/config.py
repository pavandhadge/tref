from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

APP_NAME = "tref"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
DEFAULT_TOP_K = 5

TREF_HOME = Path(os.getenv("TREF_HOME", Path.home() / ".tref"))
INDEX_ROOT = TREF_HOME / "indexes"
CUSTOM_INDEX_ROOT = TREF_HOME / "custom"
CACHE_ROOT = TREF_HOME / "cache"
MANIFEST_CACHE = CACHE_ROOT / "manifest.json"
UPDATE_STATE_CACHE = CACHE_ROOT / "update_state.json"
REMOTE_CONFIG_FILE = TREF_HOME / "remote.json"

DEFAULT_KB_MANIFEST_URL = "https://raw.githubusercontent.com/tref-org/tref-kb/main/kb/_manifest.json"
DEFAULT_RELEASES_API_URL = "https://api.github.com/repos/tref-org/tref-kb/releases/latest"
DEFAULT_RELEASE_ASSET_NAME = "tref-indexes.tar.gz"
DEFAULT_RELEASE_CHECKSUM_ASSET_NAME = "tref-indexes.tar.gz.sha256"

OLLAMA_URL = os.getenv("TREF_OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
MAX_INDEX_AGE_DAYS = int(os.getenv("TREF_MAX_INDEX_AGE_DAYS", "7"))
HTTP_TIMEOUT_SECONDS = float(os.getenv("TREF_HTTP_TIMEOUT_SECONDS", "20"))
HTTP_MAX_RETRIES = int(os.getenv("TREF_HTTP_MAX_RETRIES", "3"))
HTTP_RETRY_BACKOFF_SECONDS = float(os.getenv("TREF_HTTP_RETRY_BACKOFF_SECONDS", "0.5"))
UPDATE_STRICT_VERIFY = os.getenv("TREF_UPDATE_STRICT_VERIFY", "1") == "1"
MAX_DOWNLOAD_BYTES = int(os.getenv("TREF_MAX_DOWNLOAD_BYTES", str(1024 * 1024 * 1024)))


def ensure_dirs() -> None:
    INDEX_ROOT.mkdir(parents=True, exist_ok=True)
    CUSTOM_INDEX_ROOT.mkdir(parents=True, exist_ok=True)
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)


def load_remote_config() -> dict[str, Any]:
    ensure_dirs()
    if not REMOTE_CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(REMOTE_CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_remote_config(data: dict[str, Any]) -> None:
    ensure_dirs()
    _atomic_write_json(REMOTE_CONFIG_FILE, data)


def reset_remote_config() -> None:
    ensure_dirs()
    if REMOTE_CONFIG_FILE.exists():
        REMOTE_CONFIG_FILE.unlink()


def get_kb_manifest_url() -> str:
    return os.getenv("TREF_KB_MANIFEST_URL") or load_remote_config().get("kb_manifest_url") or DEFAULT_KB_MANIFEST_URL


def get_releases_api_url() -> str:
    return os.getenv("TREF_RELEASES_API") or load_remote_config().get("releases_api_url") or DEFAULT_RELEASES_API_URL


def get_release_asset_name() -> str:
    return os.getenv("TREF_RELEASE_ASSET") or load_remote_config().get("release_asset_name") or DEFAULT_RELEASE_ASSET_NAME


def get_release_checksum_asset_name() -> str:
    return (
        os.getenv("TREF_RELEASE_CHECKSUM_ASSET")
        or load_remote_config().get("release_checksum_asset_name")
        or DEFAULT_RELEASE_CHECKSUM_ASSET_NAME
    )


def get_remote_settings() -> dict[str, Any]:
    return {
        "kb_manifest_url": get_kb_manifest_url(),
        "releases_api_url": get_releases_api_url(),
        "release_asset_name": get_release_asset_name(),
        "release_checksum_asset_name": get_release_checksum_asset_name(),
        "strict_verify": UPDATE_STRICT_VERIFY,
        "remote_config_file": str(REMOTE_CONFIG_FILE),
    }
