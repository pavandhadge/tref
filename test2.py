#!/usr/bin/env python3
import os
import json
import argparse
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# === Configuration ===
CONFIG_DIR_NAME = "tref"
DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
CHUNK_SIZE = 256  # Larger batch size for faster processing
CACHE_SIZE = 200  # Increased query cache
TOP_K = 5  # Default results to show

class CheatManager:
    # Singleton model instance
    _model_instance = None
    _tokenizer_instance = None

    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.cheatsheets_dir = self.config_dir / "cheatsheets"
        self.embeddings_file = self.config_dir / "vectors.npy"
        self.meta_file = self.config_dir / "meta.jsonl"

        self.cheatsheets_dir.mkdir(parents=True, exist_ok=True)

        # Performance-critical in-memory data
        self._embeddings = None
        self._metadata = None
        self._tool_indices = {}
        self._query_cache = {}
        self._device = self._get_device()

        # Load model and data immediately
        self._load_model()
        self._load_data()

    @classmethod
    def _load_model(cls):
        """Load model once and cache it"""
        if cls._model_instance is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            cls._model_instance = AutoModel.from_pretrained(
                DEFAULT_MODEL,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True
            ).eval().to(device)

        if cls._tokenizer_instance is None:
            cls._tokenizer_instance = AutoTokenizer.from_pretrained(DEFAULT_MODEL)

        return cls._model_instance, cls._tokenizer_instance

    def _get_device(self):
        """Determine best available device"""
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        return 'cpu'

    def _get_config_dir(self) -> Path:
        """Get platform-appropriate config directory"""
        system = platform.system()
        if system == "Windows":
            base = Path(os.getenv('APPDATA', ''))
        else:
            base = Path(os.getenv('XDG_CONFIG_HOME', Path.home() / '.config'))
        return base / CONFIG_DIR_NAME

    def _load_data(self):
        """Load all data into memory for fastest access"""
        if not self.embeddings_file.exists() or not self.meta_file.exists():
            return

        # Load embeddings into memory (not memory-mapped)
        self._embeddings = np.load(self.embeddings_file)

        # Load metadata in one read
        with open(self.meta_file, 'r') as f:
            self._metadata = [json.loads(line) for line in f]

    def encode_query(self, query: str) -> np.ndarray:
        """Optimized query encoding with caching"""
        if query in self._query_cache:
            return self._query_cache[query]

        model, tokenizer = self._load_model()

        inputs = tokenizer(
            query,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        ).to(self._device)

        with torch.no_grad():
            outputs = model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
            embedding = embedding.astype(np.float16)

        # Update cache
        if len(self._query_cache) >= CACHE_SIZE:
            self._query_cache.pop(next(iter(self._query_cache)))
        self._query_cache[query] = embedding

        return embedding

    def _fast_cosine_similarity(self, query: np.ndarray, targets: np.ndarray) -> np.ndarray:
        """Ultra-optimized cosine similarity using NumPy"""
        # Pre-normalized embeddings, so just dot product
        return np.dot(targets, query.T).flatten()

    def _get_tool_indices(self, tool: str) -> np.ndarray:
        """Get indices for a tool with caching"""
        if tool in self._tool_indices:
            return self._tool_indices[tool]

        if self._metadata is None:
            raise ValueError("Metadata not loaded")

        indices = [
            i for i, m in enumerate(self._metadata)
            if m['tool'].lower() == tool.lower()
        ]
        self._tool_indices[tool] = indices
        return indices

    def semantic_search(self, tool: str, query: str, top_k: int = TOP_K) -> List[Dict]:
        """Instant semantic search with all optimizations"""
        try:
            if self._embeddings is None or self._metadata is None:
                raise ValueError("Embeddings not loaded. Run --update-embeddings first")

            relevant_indices = self._get_tool_indices(tool)
            if not relevant_indices:
                return []

            relevant_embeddings = self._embeddings[relevant_indices]
            query_embedding = self.encode_query(query)

            # Fastest possible similarity calculation
            scores = self._fast_cosine_similarity(query_embedding, relevant_embeddings)

            # Optimized top-k selection
            if len(scores) <= top_k:
                top_indices = np.argsort(scores)[::-1]
            else:
                top_indices = np.argpartition(scores, -top_k)[-top_k:]
                top_indices = top_indices[np.argsort(scores[top_indices])[::-1]]

            # Direct result construction
            return [{
                'name': self._metadata[relevant_indices[i]]['name'],
                'command': self._metadata[relevant_indices[i]]['command'],
                'explanation': self._metadata[relevant_indices[i]]['explanation'],
                'score': float(scores[i])
            } for i in top_indices]

        except Exception as e:
            print(f"Search error: {e}")
            return []

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
        model, tokenizer = self._load_model()

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

        # Process in large batches
        embeddings = []
        for i in range(0, len(texts), CHUNK_SIZE):
            chunk = texts[i:i + CHUNK_SIZE]

            inputs = tokenizer(
                chunk,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=256
            ).to(self._device)

            with torch.no_grad():
                outputs = model(**inputs)
                chunk_emb = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                chunk_emb = chunk_emb / np.linalg.norm(chunk_emb, axis=1, keepdims=True)
                embeddings.append(chunk_emb.astype(np.float16))

        # Save results
        full_embeddings = np.vstack(embeddings)
        np.save(self.embeddings_file, full_embeddings)

        with open(self.meta_file, 'w') as f:
            for idx, entry in enumerate(entries):
                entry['index'] = idx
                f.write(json.dumps(entry) + '\n')

        # Reload the new data
        self._load_data()
        self._tool_indices.clear()
        self._query_cache.clear()

        print(f"Generated {len(entries)} embeddings from {len(self.list_cheatsheets())} cheat sheets")

    def interactive_search(self):
        """Interactive search interface"""
        print("Available tools:", ", ".join(self.list_cheatsheets()))

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
    main()