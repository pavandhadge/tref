import argparse
import sys
import numpy as np
import json
from pathlib import Path
from tref.cheatsheet import CheatSheetManager
from tref.embeddings import EmbeddingManager
from tref.search import SearchManager
from tref.config import get_config_dir


def load_embeddings_and_meta(config_dir: Path):
    embeddings_file = config_dir / "vectors.npy"
    meta_file = config_dir / "meta.jsonl"
    if not embeddings_file.exists() or not meta_file.exists():
        return None, None
    embeddings = np.load(embeddings_file)
    with open(meta_file, 'r') as f:
        metadata = [json.loads(line) for line in f]
    return embeddings, metadata

def update_embeddings(manager: CheatSheetManager, emb_mgr: EmbeddingManager, config_dir: Path):
    print("Generating embeddings from cheat sheets...")
    entries = []
    texts = []
    for tool in manager.list_cheatsheets():
        try:
            content = manager.read_cheatsheet(tool)
            tool_name = next(iter(content))
            sections = content[tool_name]
            for section, items in sections.items():
                for item in items:
                    entries.append({
                        'tool': tool_name.replace(" Cheatsheet", "").lower(),
                        'name': item['name'],
                        'command': item['command'],
                        'explanation': item['explanation'],
                        'tags': item.get('tags', []) + [section]
                    })
                    texts.append(f"{item['name']} {item['explanation']}")
        except Exception as e:
            print(f"Skipping {tool}: {e}")
            continue
    if not entries:
        print("No valid cheat sheets found to process")
        return
    full_embeddings = emb_mgr.encode_batch(texts)
    np.save(config_dir / "vectors.npy", full_embeddings)
    with open(config_dir / "meta.jsonl", 'w') as f:
        for idx, entry in enumerate(entries):
            entry['index'] = idx
            f.write(json.dumps(entry) + '\n')
    print(f"Generated {len(entries)} embeddings from {len(manager.list_cheatsheets())} cheat sheets")

def interactive_search(manager: CheatSheetManager, search_mgr: SearchManager):
    print("Available tools:", ", ".join(manager.list_cheatsheets()))
    while True:
        try:
            tool = input("\nEnter tool name (or 'quit'): ").strip()
            if tool.lower() in ('quit', 'exit', 'q'):
                break
            if tool not in manager.list_cheatsheets():
                print(f"No cheat sheet for '{tool}'. Available: {', '.join(manager.list_cheatsheets())}")
                continue
            query = input("Enter your query: ").strip()
            if not query:
                continue
            results = search_mgr.semantic_search(tool, query)
            if not results:
                print("\nNo results found")
                continue
            print("\nTop results:")
            for i, res in enumerate(results, 1):
                print(f"\n{i}. {res['name']} (Score: {res['score']:.3f})")
                print(f"   Command: {res['command']}")
                print(f"   Explanation: {res['explanation']}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Cheat sheet manager with semantic search",
        usage="%(prog)s [command] [options]"
    )
    parser.add_argument('--list', action='store_true', help='List all cheat sheets')
    parser.add_argument('--read', metavar='TOOL', help='Read a cheat sheet')
    parser.add_argument('--edit', metavar='TOOL', help='Edit a cheat sheet')
    parser.add_argument('--add', metavar='TOOL', help='Add a new cheat sheet')
    parser.add_argument('--delete', metavar='TOOL', help='Delete a cheat sheet')
    parser.add_argument('--search', nargs=2, metavar=('TOOL', 'QUERY'), help='Search a cheat sheet')
    parser.add_argument('--interactive', action='store_true', help='Launch interactive search')
    parser.add_argument('--update-embeddings', action='store_true', help='Update embeddings from cheat sheets')
    args = parser.parse_args()
    manager = CheatSheetManager()
    emb_mgr = EmbeddingManager()
    config_dir = get_config_dir()
    try:
        if args.list:
            print("Available cheat sheets:")
            for sheet in manager.list_cheatsheets():
                print(f"- {sheet}")
        elif args.read:
            manager.show_cheatsheet(args.read)
        elif args.edit:
            manager.edit_cheatsheet(args.edit)
        elif args.add:
            manager.add_cheatsheet(args.add)
        elif args.delete:
            manager.delete_cheatsheet(args.delete)
        elif args.search:
            embeddings, metadata = load_embeddings_and_meta(config_dir)
            if embeddings is None or metadata is None:
                print("No embeddings found. Run --update-embeddings first.")
                return
            search_mgr = SearchManager(embeddings, metadata)
            results = search_mgr.semantic_search(args.search[0], args.search[1])
            if not results:
                print("No results found")
            else:
                print(f"Top results for '{args.search[1]}':")
                for i, res in enumerate(results, 1):
                    print(f"\n{i}. {res['name']} (Score: {res['score']:.3f})")
                    print(f"   Command: {res['command']}")
                    print(f"   Explanation: {res['explanation']}")
        elif args.interactive:
            embeddings, metadata = load_embeddings_and_meta(config_dir)
            if embeddings is None or metadata is None:
                print("No embeddings found. Run --update-embeddings first.")
                return
            search_mgr = SearchManager(embeddings, metadata)
            interactive_search(manager, search_mgr)
        elif args.update_embeddings:
            update_embeddings(manager, emb_mgr, config_dir)
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
