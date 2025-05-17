package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
)

func getCheatConfigDir() string {
	var configDir string

	if runtime.GOOS != "windows" {
		if xdg := os.Getenv("XDG_CONFIG_HOME"); xdg != "" {
			configDir = filepath.Join(xdg, "tref")
		} else {
			home, err := os.UserHomeDir()
			if err != nil {
				fmt.Println("Failed to get home directory:", err)
				os.Exit(1)
			}
			configDir = filepath.Join(home, ".config", "tref")
		}
	} else {
		if appData := os.Getenv("AppData"); appData != "" {
			configDir = filepath.Join(appData, "tref")
		} else {
			fmt.Println("No valid config directory found")
			os.Exit(1)
		}
	}

	if err := os.MkdirAll(configDir, 0755); err != nil {
		fmt.Println("Failed to create config directory:", err)
		os.Exit(1)
	}

	return configDir
}

func openEditor(filePath, editor string) error {
	cmd := exec.Command(editor, filePath)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func readCheatSheet(args []string) {
	if len(args) < 1 {
		fmt.Println("Please provide a tool name to read.")
		os.Exit(1)
	}
	configDir := getCheatConfigDir()
	filePath := filepath.Join(configDir, args[0]+".json")

	data, err := os.ReadFile(filePath)
	if err != nil {
		fmt.Printf("Failed to read cheat sheet for '%s': %v\n", args[0], err)
		os.Exit(1)
	}

	fmt.Printf("Cheat Sheet for %s:\n%s\n", args[0], string(data))
}

func editCheatSheet(args []string) {
	if len(args) < 1 {
		fmt.Println("Please provide a tool name to edit.")
		os.Exit(1)
	}
	configDir := getCheatConfigDir()
	filePath := filepath.Join(configDir, args[0]+".json")

	editor := os.Getenv("EDITOR")
	if editor == "" {
		editor = "nano"
	}

	if err := openEditor(filePath, editor); err != nil {
		fmt.Println("Failed to open editor:", err)
		os.Exit(1)
	}
}

func addCheatSheet(args []string) {
	if len(args) < 1 {
		fmt.Println("Please provide a tool name to add.")
		os.Exit(1)
	}
	configDir := getCheatConfigDir()
	filePath := filepath.Join(configDir, args[0]+".json")

	file, err := os.Create(filePath)
	if err != nil {
		fmt.Printf("Error creating file %s: %v\n", filePath, err)
		os.Exit(1)
	}
	defer file.Close()

	editor := os.Getenv("EDITOR")
	if editor == "" {
		editor = "nano"
	}

	if err := openEditor(filePath, editor); err != nil {
		fmt.Println("Failed to open editor:", err)
		os.Exit(1)
	}
}

func deleteCheatSheet(args []string) {
	if len(args) < 1 {
		fmt.Println("Please provide a tool name to delete.")
		os.Exit(1)
	}
	configDir := getCheatConfigDir()
	filePath := filepath.Join(configDir, args[0]+".json")

	if err := os.Remove(filePath); err != nil {
		fmt.Printf("Error deleting file %s: %v\n", filePath, err)
		os.Exit(1)
	}

	fmt.Println("Cheat sheet deleted successfully.")
}

func helpFunc() {
	fmt.Print(`Usage: tref <toolname> [--read|--edit|--add|--delete|--help]

Available Commands:
  --read      Read an existing cheat sheet
  --edit      Edit an existing cheat sheet
  --add       Create a new cheat sheet
  --delete    Delete an existing cheat sheet
  --help      Show this help message

Examples:
  tref git --read       # View cheat sheet for git
  tref curl --edit      # Edit cheat sheet for curl
  tref make --add       # Create a new cheat sheet for make
  tref ls --delete      # Delete cheat sheet for ls
  tref --help           # Show usage help
`)
}

func main() {
	args := os.Args[1:]
	if len(args) < 1 {
		fmt.Println("Usage: tref <toolname> [--read|--edit|--add|--delete]")
		os.Exit(1)
	}

	if args[0] == "--help" {
		helpFunc()
		os.Exit(0)
	}
	mode := "--read"
	if len(args) >= 2 {
		mode = args[1]
	}

	switch mode {
	case "--read":
		readCheatSheet(args)
	case "--edit":
		editCheatSheet(args)
	case "--add":
		addCheatSheet(args)
	case "--delete":
		deleteCheatSheet(args)
	default:
		fmt.Printf("Invalid mode selected: %s\n", mode)
		os.Exit(1)
	}
}
