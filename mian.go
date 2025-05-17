Here's a complete and updated `README.md` for your `tref` cheat config tool based on the code you provided:

---

# `tref` – Terminal Reference Manager

`tref` is a command-line utility to manage personal **cheat sheets** for different developer tools. It provides quick access to custom or default command references, config snippets, and usage examples — all stored locally in OS-specific configuration directories.

## ✨ Features

* 📖 Read (`--read`) cheat sheets
* 📝 Edit (`--edit`) cheat sheets using your terminal editor
* 🆕 Add (`--add`) new cheat sheets
* ❌ Delete (`--delete`) existing cheat sheets
* 🔁 Reset to defaults (`--reset` or `--get-default`) from GitHub
* ❓ Display help info (`--help`)

## 📁 Cheat Sheet Storage

Cheat sheets are stored in an OS-specific config directory under `tref/`:

| OS      | Config Directory                            |
| ------- | ------------------------------------------- |
| Linux   | `$XDG_CONFIG_HOME/tref` or `~/.config/tref` |
| macOS   | `$XDG_CONFIG_HOME/tref` or `~/.config/tref` |
| Windows | `%AppData%\tref`                            |

Each cheat sheet is stored as a `toolname.json` file.

## 🛠 Usage

```bash
tref <toolname> [--read | --edit | --add | --delete]
```

Or for global operations:

```bash
tref [--reset | --get-default | --help]
```

### ✅ Examples

```bash
# View a cheat sheet for git
tref git --read

# Edit a cheat sheet for docker
tref docker --edit

# Create a new cheat sheet for kubectl
tref kubectl --add

# Delete an existing cheat sheet for terraform
tref terraform --delete

# Reset all cheat sheets to official defaults
tref --reset

# Get help/usage info
tref --help
```

## 🔄 Reset to Defaults

You can fetch a full set of prebuilt cheat sheets from the following GitHub JSON:

```
https://raw.githubusercontent.com/pavandhadge/tref/main/defaultCheatsheets/devtools.json
```

Use either of the following to reset your cheat sheets:

```bash
tref --reset
# or
tref --get-default
```

This will:

* Download the JSON
* Wipe your existing local cheat sheets
* Split the master file into individual `<tool>.json` files

## 🖋 Environment Variables

* `EDITOR`: Used to open `.json` files for `--edit` and `--add`.

  * Defaults to `nano` if not set.

## ⚙ Functions Overview

| Function                        | Description                                            |
| ------------------------------- | ------------------------------------------------------ |
| `getCheatConfigDir()`           | Detects OS and returns/creates the correct config path |
| `readCheatSheet(args)`          | Displays contents of a cheat sheet                     |
| `editCheatSheet(args)`          | Opens a cheat sheet for editing in terminal editor     |
| `addCheatSheet(args)`           | Creates a new cheat sheet and opens it for editing     |
| `deleteCheatSheet(args)`        | Removes a cheat sheet                                  |
| `downloadAndSplitCheatSheets()` | Downloads master JSON and splits into individual files |
| `cleanConfigDir()`              | Clears all current cheat sheets from config directory  |

## ❌ Error Handling

* Graceful exit and message if:

  * Required tool name is missing
  * File operations fail
  * Invalid command is given
* Automatically creates config directory if not found

---

This tool is ideal for developers who prefer **fast terminal-based access** to curated command references without browsing the web or switching context.

> Built for speed. Works offline. Lives in your terminal.
