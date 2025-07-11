# tref Architecture

`tref` is a modular Python CLI application for managing and searching developer cheat sheets with semantic search. The architecture is designed for clarity, extensibility, and performance.

## Directory Structure

```
tref/
  cheatsheet.py      # CRUD for cheat sheets
  embeddings.py      # Embedding/model logic
  search.py          # Semantic search logic
  cli.py             # CLI entry point
  config.py          # Config and device helpers
```

## Module Overview

- **cheatsheet.py**: Handles all operations for creating, reading, editing, and deleting cheat sheets. Stores data as JSON files in a user config directory.
- **embeddings.py**: Loads the transformer model, encodes text, and manages batch embedding generation for semantic search.
- **search.py**: Provides fast, in-memory semantic search using cosine similarity and efficient top-k selection.
- **cli.py**: Parses command-line arguments, routes commands, and provides the user interface.
- **config.py**: Determines the config directory and best available device (CPU, CUDA, MPS).

## Data Flow

1. **User runs a CLI command** (e.g., `--search git clone`)
2. **cli.py** parses the command and calls the appropriate manager (cheatsheet, embeddings, search)
3. **cheatsheet.py** loads or modifies JSON files as needed
4. **embeddings.py** encodes queries and cheat sheet entries using a transformer model
5. **search.py** computes semantic similarity and returns results
6. **Results are printed to the terminal**

## Design Decisions

- **Separation of concerns**: Each module has a single responsibility
- **In-memory performance**: Embeddings and metadata are loaded into memory for fast search
- **Extensible**: New features (e.g., web UI, sync) can be added by extending the CLI and managers
- **Local-first**: All data is stored and processed locally for privacy

## Example Data Files

- `~/.config/tref/cheatsheets/git.json`: Stores the user's git cheat sheet
- `~/.config/tref/vectors.npy`: Stores all embeddings for semantic search
- `~/.config/tref/meta.jsonl`: Stores metadata for each command/snippet

---

For more, see the [Command Reference](./interface.md) and [Tools Used](./tools.md). 