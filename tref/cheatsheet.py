from __future__ import annotations

import json
from pathlib import Path


class CheatSheetManager:
    """Minimal file manager for KB markdown/json assets."""

    def __init__(self, root: Path):
        self.root = root

    def list_assets(self) -> list[Path]:
        return sorted(self.root.rglob("*.md")) + sorted(self.root.rglob("*.json"))

    def read_json(self, path: Path):
        return json.loads(path.read_text(encoding="utf-8"))
