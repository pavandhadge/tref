#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from tref.indexer import validate_kb


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate tref KB markdown schema")
    parser.add_argument("kb_path", type=Path, help="Path to KB root")
    args = parser.parse_args()

    result = validate_kb(args.kb_path)
    print(json.dumps(result, indent=2))
    if not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
