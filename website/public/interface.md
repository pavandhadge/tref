# tref CLI Interface & Commands

`tref` provides a powerful, Python-based CLI for managing and searching developer cheat sheets.

## Command Reference

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

## Example Workflows

### Add and Edit a Cheat Sheet
```bash
python3 -m tref.cli --add git
python3 -m tref.cli --edit git
```

### Read a Cheat Sheet
```bash
python3 -m tref.cli --read git
```

### List All Cheat Sheets
```bash
python3 -m tref.cli --list
```

### Semantic Search
```bash
python3 -m tref.cli --search git "clone repository"
```

### Interactive Search
```bash
python3 -m tref.cli --interactive
```

### Update Embeddings
```bash
python3 -m tref.cli --update-embeddings
```

## Cheat Sheet Format

Cheat sheets are stored as JSON files. Example:

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

## Environment Variables

- `EDITOR`: Used to open `.json` files for `--edit` and `--add`. Defaults to `nano` if not set.

## Error Handling

- Graceful exit and message if required tool name is missing, file operations fail, or invalid command is given.
- Automatically creates config directory if not found.

---

For more, see the [Architecture](./architecture.md) and [Tools Used](./tools.md). 