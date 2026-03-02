#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tref.indexer import build_indexes


def main() -> None:
    parser = argparse.ArgumentParser(description="Build tref FAISS indexes from KB markdown files")
    parser.add_argument("kb_path", type=Path, help="Path to kb root")
    parser.add_argument("--output", type=Path, required=True, help="Output index root")
    args = parser.parse_args()

    summary = build_indexes(kb_root=args.kb_path, output_root=args.output)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
