# tref – Terminal Reference Manager (Python Edition)

`tref` is a modern, Python-powered command-line utility to manage personal **cheat sheets** for developer tools. It provides instant, semantic search over your custom or default command references, config snippets, and usage examples — all stored locally and privately.

---

## ✨ Features

- 📖 **Read** (`--read TOOL`) cheat sheets
- 📝 **Edit** (`--edit TOOL`) cheat sheets using your terminal editor
- 🆕 **Add** (`--add TOOL`) new cheat sheets
- ❌ **Delete** (`--delete TOOL`) existing cheat sheets
- 🔍 **Semantic Search** (`--search TOOL QUERY`) for commands by meaning
- 💬 **Interactive Search** (`--interactive`) for conversational lookup
- 🧠 **Update Embeddings** (`--update-embeddings`) after editing sheets
- 🗂 **List** (`--list`) all available cheat sheets

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install torch transformers numpy
```

### 2. Run tref

```bash
python3 -m tref.cli --help
```

### 3. Example Usage

```bash
# Add a new cheat sheet for git
python3 -m tref.cli --add git

# Edit the cheat sheet for git
python3 -m tref.cli --edit git

# Read the cheat sheet for git
python3 -m tref.cli --read git

# List all cheat sheets
python3 -m tref.cli --list

# Search for a command by meaning
python3 -m tref.cli --search git "clone repository"

# Interactive search
python3 -m tref.cli --interactive

# Update semantic embeddings after editing
python3 -m tref.cli --update-embeddings
```

## 🧩 Cheat Sheet Storage

Cheat sheets are stored in your OS-specific config directory under `tref/cheatsheets/`:

| OS      | Config Directory                            |
| ------- | ------------------------------------------- |
| Linux   | `$XDG_CONFIG_HOME/tref` or `~/.config/tref` |
| macOS   | `$XDG_CONFIG_HOME/tref` or `~/.config/tref` |
| Windows | `%AppData%\tref`                            |

Each cheat sheet is a `tool.json` file (e.g., `git.json`).

## 🧠 Semantic Search & Embeddings

- Uses [HuggingFace Transformers](https://huggingface.co/BAAI/bge-small-en-v1.5) for state-of-the-art semantic search.
- After adding or editing cheat sheets, run `--update-embeddings` to refresh the search index.
- Embeddings and metadata are stored in your config directory as `vectors.npy` and `meta.jsonl`.

## 🖋 Environment Variables

- `EDITOR`: Used to open `.json` files for `--edit` and `--add`.
  - Defaults to `nano` if not set.

## ⚙️ Command Reference

| Command/Flag                | Description                                      |
|-----------------------------|--------------------------------------------------|
| `--list`                    | List all cheat sheets                            |
| `--read TOOL`               | Read a cheat sheet                               |
| `--edit TOOL`               | Edit a cheat sheet                               |
| `--add TOOL`                | Add a new cheat sheet                            |
| `--delete TOOL`             | Delete a cheat sheet                             |
| `--search TOOL QUERY`       | Semantic search for a command                    |
| `--interactive`             | Interactive search session                       |
| `--update-embeddings`       | Update semantic search embeddings                |

## 🛠 Architecture Overview

- **tref/cheatsheet.py**: CRUD operations for cheat sheets
- **tref/embeddings.py**: Model loading and embedding generation
- **tref/search.py**: Semantic search logic
- **tref/cli.py**: CLI entry point and argument parsing
- **tref/config.py**: Config directory and device selection

## 🧪 Example Cheat Sheet Format

```json
{
  "git Cheatsheet": {
    "General": [
      {
        "name": "Clone a repository",
        "command": "git clone <url>",
        "explanation": "Clone a remote repository",
        "tags": ["clone", "remote"]
      }
    ]
  }
}
```

## ❌ Error Handling

- Graceful exit and message if:
  - Required tool name is missing
  - File operations fail
  - Invalid command is given
- Automatically creates config directory if not found

## 🔒 Privacy & Security

- All data is stored locally. No data is sent to the cloud.
- Embeddings and cheat sheets are private to your machine.

## 🧑‍💻 Contributing

Contributions are welcome! Please open issues or pull requests for improvements, bug fixes, or new features.

## 📄 License

MIT License. See [LICENSE](./LICENSE) for details.

---

> Built for speed. Works offline. Lives in your terminal. Now with semantic search.
