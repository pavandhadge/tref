# tref CLI Interface & Commands

`tref` provides a powerful, Python-based CLI for managing and searching developer cheat sheets.

## Command Reference

Below are the main commands and flags you can use with tref:

- **--list**
  - List all available cheat sheets.
  - Example:
    ```bash
    python3 -m tref.cli --list
    ```

- **--read TOOL**
  - Read and display the contents of a cheat sheet for the specified tool.
  - Example:
    ```bash
    python3 -m tref.cli --read git
    ```

- **--edit TOOL**
  - Edit a cheat sheet for the specified tool using your default terminal editor.
  - Example:
    ```bash
    python3 -m tref.cli --edit git
    ```

- **--add TOOL**
  - Add a new cheat sheet for the specified tool. If it already exists, it will open for editing.
  - Example:
    ```bash
    python3 -m tref.cli --add docker
    ```

- **--delete TOOL**
  - Delete the cheat sheet for the specified tool.
  - Example:
    ```bash
    python3 -m tref.cli --delete terraform
    ```

- **--search TOOL QUERY**
  - Perform a semantic search for a command or snippet in the specified tool's cheat sheet.
  - Example:
    ```bash
    python3 -m tref.cli --search git "clone repository"
    ```

- **--interactive**
  - Launch an interactive session to search and explore cheat sheets conversationally.
  - Example:
    ```bash
    python3 -m tref.cli --interactive
    ```

- **--update-embeddings**
  - Update the semantic search embeddings after adding or editing cheat sheets. Run this to refresh the search index.
  - Example:
    ```bash
    python3 -m tref.cli --update-embeddings
    ```

## Example Workflows

- **Add and Edit a Cheat Sheet**
  ```bash
  python3 -m tref.cli --add git
  python3 -m tref.cli --edit git
  ```

- **Read a Cheat Sheet**
  ```bash
  python3 -m tref.cli --read git
  ```

- **List All Cheat Sheets**
  ```bash
  python3 -m tref.cli --list
  ```

- **Semantic Search**
  ```bash
  python3 -m tref.cli --search git "clone repository"
  ```

- **Interactive Search**
  ```bash
  python3 -m tref.cli --interactive
  ```

- **Update Embeddings**
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