#!/usr/bin/env python3
import os
import json
import argparse
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

# === Configuration ===
CONFIG_DIR_NAME = "tref"
DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
CHUNK_SIZE = 64  # For memory-efficient processing

class CheatManager:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.cheatsheets_dir = self.config_dir / "cheatsheets"
        self.embeddings_file = self.config_dir / "vectors.npy"
        self.meta_file = self.config_dir / "meta.jsonl"

        # Create directories if they don't exist
        self.cheatsheets_dir.mkdir(parents=True, exist_ok=True)

        # Lazily loaded components
        self._encoder = None
        self._embeddings = None
        self._metadata = None
        self._interactive_mode = False  # Track if we're in interactive mode

    def _get_config_dir(self) -> Path:
        """Get platform-appropriate config directory"""
        system = platform.system()
        if system == "Windows":
            base = Path(os.getenv('APPDATA', ''))
        else:  # Unix-like
            base = Path(os.getenv('XDG_CONFIG_HOME', Path.home() / '.config'))
        return base / CONFIG_DIR_NAME

    @property
    def encoder(self):
        """Lazy-loaded sentence encoder"""
        if self._encoder is None:
            self._encoder = self._init_encoder()
        return self._encoder

    def _init_encoder(self):
        """Initialize the minimal sentence encoder"""
        from transformers import AutoTokenizer, AutoModel
        import torch

        device = 'cpu'
        tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
        model = AutoModel.from_pretrained(DEFAULT_MODEL).to(device)
        model.eval()

        class EncoderWrapper:
            def encode(self, texts: List[str], normalize: bool = True) -> np.ndarray:
                inputs = tokenizer(
                    texts,
                    padding=True,
                    truncation=True,
                    return_tensors="pt",
                    max_length=256
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()

                if normalize:
                    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

                return embeddings.astype(np.float16)

        return EncoderWrapper()

    def _cosine_similarity(self, query: np.ndarray, targets: np.ndarray) -> np.ndarray:
        """Optimized cosine similarity calculation"""
        norm_query = np.linalg.norm(query)
        norm_targets = np.linalg.norm(targets, axis=1)
        return np.dot(targets, query.T).flatten() / (norm_query * norm_targets)

    # === Cheat Sheet Management ===
    def list_cheatsheets(self) -> List[str]:
        """List all available cheat sheets"""
        return [f.stem for f in self.cheatsheets_dir.glob("*.json")]

    def read_cheatsheet(self, tool: str) -> Dict:
        """Read a cheat sheet"""
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"No cheat sheet found for '{tool}'")

        with open(filepath, 'r') as f:
            return json.load(f)

    def edit_cheatsheet(self, tool: str):
        """Edit a cheat sheet using default editor"""
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"No cheat sheet found for '{tool}'")

        editor = os.getenv('EDITOR', 'nano')
        subprocess.run([editor, str(filepath)], check=True)

    def add_cheatsheet(self, tool: str):
        """Add a new cheat sheet"""
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if filepath.exists():
            print(f"Cheat sheet for '{tool}' already exists. Opening for editing.")

        # Create default structure
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
        """Delete a cheat sheet"""
        filepath = self.cheatsheets_dir / f"{tool}.json"
        if not filepath.exists():
            raise FileNotFoundError(f"No cheat sheet found for '{tool}'")

        filepath.unlink()
        print(f"Deleted cheat sheet for '{tool}'")

    def show_cheatsheet(self, tool: str):
        """Display cheat sheet contents"""
        try:
            content = self.read_cheatsheet(tool)
            print(f"=== Cheat Sheet for {tool} ===")
            print(json.dumps(content, indent=2))
        except Exception as e:
            print(f"Error: {e}")

    # === Embedding Management ===
    def update_embeddings(self):
        """Generate embeddings from all cheat sheets"""
        print("Generating embeddings from cheat sheets...")

        # Collect all entries
        entries = []
        texts = []

        for tool in self.list_cheatsheets():
            try:
                content = self.read_cheatsheet(tool)
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

        # Process in chunks to minimize memory usage
        embeddings = []
        for i in range(0, len(texts), CHUNK_SIZE):
            chunk = texts[i:i + CHUNK_SIZE]
            embeddings.append(self.encoder.encode(chunk))

        # Save results
        full_embeddings = np.vstack(embeddings)
        np.save(self.embeddings_file, full_embeddings)

        with open(self.meta_file, 'w') as f:
            for idx, entry in enumerate(entries):
                entry['index'] = idx
                f.write(json.dumps(entry) + '\n')

        print(f"Generated {len(entries)} embeddings from {len(self.list_cheatsheets())} cheat sheets")

    def _load_search_data(self):
        """Lazy-load the search data"""
        if not self.embeddings_file.exists() or not self.meta_file.exists():
            raise FileNotFoundError("Embeddings not found. Run --update-embeddings first")

        if self._embeddings is None:
            self._embeddings = np.load(self.embeddings_file, mmap_mode='r')
        if self._metadata is None:
            self._metadata = []
            with open(self.meta_file, 'r') as f:
                for line in f:
                    self._metadata.append(json.loads(line))
        return self._embeddings, self._metadata

    # === Search Functionality ===
    def semantic_search(self, tool: str, query: str, top_k: int = 5) -> List[Dict]:
        """Perform semantic search on a tool's cheat sheet"""
        try:
            # Encode query
            query_embedding = self.encoder.encode([query])[0]

            # Load data
            embeddings, metadata = self._load_search_data()

            # Filter by tool first to minimize memory access
            relevant_indices = [
                i for i, m in enumerate(metadata)
                if m['tool'].lower() == tool.lower()
            ]

            if not relevant_indices:
                return []

            # Calculate scores efficiently
            scores = self._cosine_similarity(
                query_embedding,
                embeddings[relevant_indices]
            )

            # Get top results without full sort
            top_indices = np.argpartition(scores, -top_k)[-top_k:]
            top_indices = top_indices[np.argsort(scores[top_indices])[::-1]]

            return [{
                **metadata[relevant_indices[i]],
                'score': float(scores[i])
            } for i in top_indices]
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def interactive_search(self):
        """Interactive search interface with preloaded model"""
        print("Available tools:", ", ".join(self.list_cheatsheets()))

        # Preload the encoder when entering interactive mode
        self._interactive_mode = True
        _ = self.encoder  # This triggers the lazy loading

        try:
            while True:
                try:
                    tool = input("\nEnter tool name (or 'quit'): ").strip()
                    if tool.lower() in ('quit', 'exit', 'q'):
                        break

                    if tool not in self.list_cheatsheets():
                        print(f"No cheat sheet for '{tool}'. Available: {', '.join(self.list_cheatsheets())}")
                        continue

                    query = input("Enter your query: ").strip()
                    if not query:
                        continue

                    results = self.semantic_search(tool, query)

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
        finally:
            # Clean up when exiting interactive mode
            self._interactive_mode = False

def main():
    parser = argparse.ArgumentParser(
        description="Cheat sheet manager with semantic search",
        usage="%(prog)s [command] [options]"
    )

    # Cheat sheet management commands
    parser.add_argument('--list', action='store_true', help='List all cheat sheets')
    parser.add_argument('--read', metavar='TOOL', help='Read a cheat sheet')
    parser.add_argument('--edit', metavar='TOOL', help='Edit a cheat sheet')
    parser.add_argument('--add', metavar='TOOL', help='Add a new cheat sheet')
    parser.add_argument('--delete', metavar='TOOL', help='Delete a cheat sheet')

    # Search commands
    parser.add_argument('--search', nargs=2, metavar=('TOOL', 'QUERY'),
                       help='Search a cheat sheet')
    parser.add_argument('--interactive', action='store_true',
                       help='Launch interactive search')

    # Embedding management
    parser.add_argument('--update-embeddings', action='store_true',
                       help='Update embeddings from cheat sheets')

    args = parser.parse_args()
    manager = CheatManager()

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
            results = manager.semantic_search(args.search[0], args.search[1])
            if not results:
                print("No results found")
            else:
                print(f"Top results for '{args.search[1]}':")
                for i, res in enumerate(results, 1):
                    print(f"\n{i}. {res['name']} (Score: {res['score']:.3f})")
                    print(f"   Command: {res['command']}")
                    print(f"   Explanation: {res['explanation']}")

        elif args.interactive:
            manager.interactive_search()

        elif args.update_embeddings:
            manager.update_embeddings()

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    import sys
    main()
