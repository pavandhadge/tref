import os
import json
import shutil
import subprocess
import hashlib
from pathlib import Path
from typing import List, Dict
from tref.config import get_config_dir

class CheatSheetManager:
    def __init__(self):
        self.config_dir = get_config_dir()
        self.cheatsheets_dir = self.config_dir / "cheatsheets"
        self.cheatsheets_dir.mkdir(parents=True, exist_ok=True)
        self.setup_default_cheatsheets()

    def setup_default_cheatsheets(self):
        try:
            import importlib.resources as pkg_resources
        except ImportError:
            # Try backported to PY<37 `importlib_resources`.
            import importlib_resources as pkg_resources

        default_cheatsheets_dir = pkg_resources.files('tref') / 'defaultCheatsheets'
        if not default_cheatsheets_dir.is_dir():
            return
        for cheatsheet in default_cheatsheets_dir.iterdir():
            if cheatsheet.suffix == '.json':
                if not (self.cheatsheets_dir / cheatsheet.name).exists():
                    with pkg_resources.as_file(cheatsheet) as cs:
                        shutil.copy(cs, self.cheatsheets_dir)


    def get_cheatsheet_hash(self, tool: str) -> str:
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if not filepath.exists():
            return ""
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def list_cheatsheets(self) -> List[str]:
        return [f.stem for f in self.cheatsheets_dir.glob("*.json")]

    def read_cheatsheet(self, tool: str) -> Dict:
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"No cheat sheet found for '{tool}'")
        with open(filepath, 'r') as f:
            return json.load(f)

    def edit_cheatsheet(self, tool: str):
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"No cheat sheet found for '{tool}'")
        editor = os.getenv('EDITOR', 'nano')
        subprocess.run([editor, str(filepath)], check=True)

    def add_cheatsheet(self, tool: str):
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if filepath.exists():
            print(f"Cheat sheet for '{tool}' already exists. Opening for editing.")
        default_content = {
            f"{tool} Cheatsheet": {
                "General": [
                    {
                        "name": "Example Command",
                        "command": "example --option",
                        "explanation": "What this command does",
                        "tags": []
                    }
                ]
            }
        }
        with open(filepath, 'w') as f:
            json.dump(default_content, f, indent=2)
        print(f"Created new cheat sheet for '{tool}' at {filepath}")
        self.edit_cheatsheet(tool)

    def delete_cheatsheet(self, tool: str):
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"No cheat sheet found for '{tool}'")
        filepath.unlink()
        print(f"Deleted cheat sheet for '{tool}'")

    def reset_cheatsheets(self):
        for cheatsheet in self.cheatsheets_dir.glob("*.json"):
            cheatsheet.unlink()
        self.setup_default_cheatsheets()
