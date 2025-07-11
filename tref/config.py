import os
import platform
from pathlib import Path

CONFIG_DIR_NAME = "tref"
DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
CHUNK_SIZE = 256
CACHE_SIZE = 200
TOP_K = 5

def get_config_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(os.getenv('APPDATA', ''))
    else:
        base = Path(os.getenv('XDG_CONFIG_HOME', Path.home() / '.config'))
    return base / CONFIG_DIR_NAME

def get_device() -> str:
    try:
        import torch
        if torch.cuda.is_available():
            return 'cuda'
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return 'mps'
    except ImportError:
        pass
    return 'cpu' 