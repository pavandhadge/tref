# Cheat Config Tool

A command-line tool to manage cheat sheets (in JSON format) for various tools. The cheat sheets are stored in a cross-platform configuration directory, and this utility supports creating, editing, reading, and deleting these files.

## Features

* Create (`--add`) cheat sheet files
* Edit (`--edit`) existing cheat sheets
* Read (`--read`) the contents of cheat sheets
* Delete (`--delete`) cheat sheets

## File Storage

Cheat sheets are saved in the user's OS-specific configuration directory under a subdirectory named `tref`:

* Linux/macOS: `$XDG_CONFIG_HOME/tref` or `~/.config/tref`
* Windows: `%AppData%\tref`

## Usage

```bash
tref <toolname> [--read|--edit|--add|--delete]
```

### Examples

```bash
# Read a cheat sheet for "git"
tref git --read

# Edit a cheat sheet for "docker"
tref docker --edit

# Add a new cheat sheet for "kubectl"
tref kubectl --add

# Delete a cheat sheet for "terraform"
tref terraform --delete
```

## Environment Variables

* `EDITOR`: Used to open files. Defaults to `nano` if not set.

## Function Descriptions

### `getCheatConfigDir() string`

Detects and returns the correct configuration directory based on the OS. Creates the directory if it doesn't exist.

### `openEditor(filePath, editor string) error`

Spawns a subprocess to open the specified file with the provided editor.

### `readCheatSheet(args []string)`

Reads and prints the contents of a cheat sheet.

* Requires: `args[0]` as the tool name.

### `editCheatSheet(args []string)`

Opens an existing cheat sheet file in the terminal editor.

* Requires: `args[0]` as the tool name.

### `addCheatSheet(args []string)`

Creates a new cheat sheet and opens it in the editor.

* Requires: `args[0]` as the tool name.

### `deleteCheatSheet(args []string)`

Deletes an existing cheat sheet.

* Requires: `args[0]` as the tool name.

### `main()`

Parses command-line arguments and invokes the appropriate operation based on the second argument (mode).

## Error Handling

* If required arguments are missing, a helpful usage message is displayed.
* File I/O operations log fatal errors for better visibility and debugging.

---

This tool is ideal for developers who want quick terminal-based access to frequently used command references, configuration patterns, or usage examples.
