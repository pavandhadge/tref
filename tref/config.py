from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

APP_NAME = "tref"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"

TREF_HOME = Path(os.getenv("TREF_HOME", Path.home() / ".tref"))
INDEX_ROOT = TREF_HOME / "indexes"
CUSTOM_INDEX_ROOT = TREF_HOME / "custom"
CACHE_ROOT = TREF_HOME / "cache"
CONFIG_FILE = TREF_HOME / "config.json"
MANIFEST_CACHE = CACHE_ROOT / "manifest.json"
UPDATE_STATE_CACHE = CACHE_ROOT / "update_state.json"
REMOTE_CONFIG_FILE = TREF_HOME / "remote.json"

# Source of truth is pavandhadge/tref:
# - Human release page: https://github.com/pavandhadge/tref/releases/latest
# - API endpoint used by updater:
DEFAULT_KB_MANIFEST_URL = "https://raw.githubusercontent.com/pavandhadge/tref/main/kb/_manifest.json"
DEFAULT_RELEASES_API_URL = "https://api.github.com/repos/pavandhadge/tref/releases/latest"
DEFAULT_RELEASE_ASSET_NAME = "tref-indexes.tar.gz"
DEFAULT_RELEASE_CHECKSUM_ASSET_NAME = "tref-indexes.tar.gz.sha256"
DEFAULT_RELEASE_SIGNATURE_ASSET_NAME = "tref-indexes.tar.gz.sig"

DEFAULT_TOP_K = 5
DEFAULT_LLM_MODEL = "llama3.1:8b-instruct"
DEFAULT_EXAMPLE_LANG = None


def _as_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"1", "true", "yes", "on"}:
            return True
        if v in {"0", "false", "no", "off"}:
            return False
    return default


def _as_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _as_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default


def load_user_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        return {}
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_user_config(data: dict[str, Any]) -> None:
    ensure_dirs()
    _atomic_write_json(CONFIG_FILE, data)


def reset_user_config() -> None:
    ensure_dirs()
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()


def _cfg_value(config_key: str, env_key: str | None, default: Any) -> Any:
    if env_key:
        env_val = os.getenv(env_key)
        if env_val is not None:
            return env_val
    cfg = load_user_config()
    if config_key in cfg:
        return cfg[config_key]
    return default


OLLAMA_URL = str(_cfg_value("ollama_url", "TREF_OLLAMA_URL", "http://127.0.0.1:11434/api/generate"))
MAX_INDEX_AGE_DAYS = _as_int(_cfg_value("max_index_age_days", "TREF_MAX_INDEX_AGE_DAYS", 7), 7)
HTTP_TIMEOUT_SECONDS = _as_float(_cfg_value("http_timeout_seconds", "TREF_HTTP_TIMEOUT_SECONDS", 20.0), 20.0)
HTTP_MAX_RETRIES = _as_int(_cfg_value("http_max_retries", "TREF_HTTP_MAX_RETRIES", 3), 3)
HTTP_RETRY_BACKOFF_SECONDS = _as_float(
    _cfg_value("http_retry_backoff_seconds", "TREF_HTTP_RETRY_BACKOFF_SECONDS", 0.5),
    0.5,
)
UPDATE_STRICT_VERIFY = _as_bool(_cfg_value("update_strict_verify", "TREF_UPDATE_STRICT_VERIFY", True), True)
REQUIRE_SIGNATURE = _as_bool(_cfg_value("require_signature", "TREF_REQUIRE_SIGNATURE", False), False)
MAX_DOWNLOAD_BYTES = _as_int(_cfg_value("max_download_bytes", "TREF_MAX_DOWNLOAD_BYTES", 1024 * 1024 * 1024), 1024 * 1024 * 1024)
COSIGN_KEY_PATH = str(_cfg_value("cosign_key_path", "TREF_COSIGN_KEY_PATH", ""))
COSIGN_BIN = str(_cfg_value("cosign_bin", "TREF_COSIGN_BIN", "cosign"))
DEFAULT_FRESHNESS_POLICY = str(_cfg_value("freshness_policy", "TREF_FRESHNESS_POLICY", "warn"))
DEFAULT_TOP_K = _as_int(_cfg_value("top_k", None, DEFAULT_TOP_K), DEFAULT_TOP_K)
DEFAULT_LLM_MODEL = str(_cfg_value("llm_model", None, DEFAULT_LLM_MODEL))
_lang = _cfg_value("example_language", None, DEFAULT_EXAMPLE_LANG)
DEFAULT_EXAMPLE_LANG = str(_lang) if _lang else None


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
    user = load_user_config()
    return (
        os.getenv("TREF_KB_MANIFEST_URL")
        or user.get("kb_manifest_url")
        or load_remote_config().get("kb_manifest_url")
        or DEFAULT_KB_MANIFEST_URL
    )


def get_releases_api_url() -> str:
    user = load_user_config()
    return (
        os.getenv("TREF_RELEASES_API")
        or user.get("releases_api_url")
        or load_remote_config().get("releases_api_url")
        or DEFAULT_RELEASES_API_URL
    )


def get_release_asset_name() -> str:
    user = load_user_config()
    return (
        os.getenv("TREF_RELEASE_ASSET")
        or user.get("release_asset_name")
        or load_remote_config().get("release_asset_name")
        or DEFAULT_RELEASE_ASSET_NAME
    )


def get_release_checksum_asset_name() -> str:
    user = load_user_config()
    return (
        os.getenv("TREF_RELEASE_CHECKSUM_ASSET")
        or user.get("release_checksum_asset_name")
        or load_remote_config().get("release_checksum_asset_name")
        or DEFAULT_RELEASE_CHECKSUM_ASSET_NAME
    )


def get_release_signature_asset_name() -> str:
    user = load_user_config()
    return (
        os.getenv("TREF_RELEASE_SIGNATURE_ASSET")
        or user.get("release_signature_asset_name")
        or load_remote_config().get("release_signature_asset_name")
        or DEFAULT_RELEASE_SIGNATURE_ASSET_NAME
    )


def get_remote_settings() -> dict[str, Any]:
    return {
        "kb_manifest_url": get_kb_manifest_url(),
        "releases_api_url": get_releases_api_url(),
        "release_asset_name": get_release_asset_name(),
        "release_checksum_asset_name": get_release_checksum_asset_name(),
        "release_signature_asset_name": get_release_signature_asset_name(),
        "strict_verify": UPDATE_STRICT_VERIFY,
        "require_signature": REQUIRE_SIGNATURE,
        "config_file": str(CONFIG_FILE),
        "remote_config_file": str(REMOTE_CONFIG_FILE),
    }


def get_user_defaults() -> dict[str, Any]:
    return {
        "freshness_policy": DEFAULT_FRESHNESS_POLICY,
        "update_strict_verify": UPDATE_STRICT_VERIFY,
        "require_signature": REQUIRE_SIGNATURE,
        "top_k": DEFAULT_TOP_K,
        "llm_model": DEFAULT_LLM_MODEL,
        "example_language": DEFAULT_EXAMPLE_LANG,
        "max_index_age_days": MAX_INDEX_AGE_DAYS,
        "http_timeout_seconds": HTTP_TIMEOUT_SECONDS,
        "http_max_retries": HTTP_MAX_RETRIES,
        "http_retry_backoff_seconds": HTTP_RETRY_BACKOFF_SECONDS,
        "ollama_url": OLLAMA_URL,
        "max_download_bytes": MAX_DOWNLOAD_BYTES,
        "cosign_key_path": COSIGN_KEY_PATH,
        "cosign_bin": COSIGN_BIN,
        "config_file": str(CONFIG_FILE),
    }
