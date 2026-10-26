
import os
import sys
import shlex
import subprocess
from pathlib import Path
from datetime import datetime

# Mini Command-Line Shell
class MiniShell:
    def __init__(self):
        self.history = []
        self.running = True
        self.start_time = datetime.now()

    def show_help(self):
        print("""
========== MINI SHELL HELP ==========
help          - Show available commands
pwd           - Show current directory
cd <path>     - Change directory
ls / dir      - List files and folders
mkdir <name>  - Create a new directory
clear         - Clear the terminal
history       - Show command history
run <command> - Execute an external program
info          - Show shell information
exit          - Exit the shell
=====================================
""")

    def execute(self, line):
        line = line.strip()

        if not line:
            return

        self.history.append(line)

        # Split command from its arguments
        parts = line.split(maxsplit=1)
        command = parts[0].lower()
        argument = parts[1].strip() if len(parts) > 1 else ""

        if command == "help":
            self.show_help()

        elif command == "pwd":
            print(os.getcwd())

        elif command == "cd":
            if not argument:
                print("Usage: cd <directory>")
                return

            path = argument.strip("\"'")
            path = os.path.expanduser(path)

            try:
                os.chdir(path)
            except FileNotFoundError:
                print("Error: Directory not found.")
            except NotADirectoryError:
                print("Error: Path is not a directory.")
            except PermissionError:
                print("Error: Permission denied.")
            except OSError as error:
                print(f"Error: {error}")

        elif command in ("ls", "dir"):
            path = argument.strip("\"'") if argument else "."

            try:
                entries = sorted(
                    Path(path).iterdir(),
                    key=lambda item: (not item.is_dir(), item.name.lower())
                )

                if not entries:
                    print("Directory is empty.")

                for entry in entries:
                    kind = "[DIR] " if entry.is_dir() else "[FILE]"
                    print(f"{kind:7} {entry.name}")

            except FileNotFoundError:
                print("Error: Directory not found.")
            except PermissionError:
                print("Error: Permission denied.")
            except OSError as error:
                print(f"Error: {error}")

        elif command == "mkdir":
            if not argument:
                print("Usage: mkdir <directory_name>")
                return

            path = argument.strip("\"'")

            try:
                Path(path).mkdir()
                print(f"Directory created: {path}")
            except FileExistsError:
                print("Error: Directory or file already exists.")
            except OSError as error:
                print(f"Error: {error}")

        elif command == "clear":
            os.system("cls" if os.name == "nt" else "clear")

        elif command == "history":
            if not self.history:
                print("No commands entered yet.")
            else:
                for number, item in enumerate(self.history, start=1):
                    print(f"{number:3}: {item}")

        elif command == "info":
            print("\n========== SHELL INFO ==========")
            print("Name       : Python Mini Shell")
            print("Version    : 1.0")
            print("Python     :", sys.version.split()[0])
            print("Platform   :", sys.platform)
            print("Started at :", self.start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ))
            print("Directory  :", os.getcwd())
            print("================================")

        elif command == "run":
            if not argument:
                print("Usage: run <program> [arguments]")
                return

            try:
                # Run without a system shell for safer execution
                args = shlex.split(
                    argument,
                    posix=(os.name != "nt")
                )

                if not args:
                    print("Please provide a program name.")
                    return

                result = subprocess.run(args, check=False)

                if result.returncode != 0:
                    print(
                        f"Program exited with code "
                        f"{result.returncode}"
                    )

            except FileNotFoundError:
                print("Error: Program not found.")
            except PermissionError:
                print("Error: Permission denied.")
            except ValueError as error:
                print(f"Invalid command: {error}")
            except OSError as error:
                print(f"Execution error: {error}")

        elif command == "exit":
            print("Exiting Mini Shell. Goodbye!")
            self.running = False

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' to see available commands.")

    def start(self):
        print("=" * 45)
        print("       WELCOME TO PYTHON MINI SHELL")
        print("=" * 45)
        print("Type 'help' to see available commands.")
        print("Type 'exit' to quit.\n")

        while self.running:
            try:
                current_dir = os.getcwd()
                prompt_dir = os.path.basename(current_dir)
                if not prompt_dir:
                    prompt_dir = current_dir

                line = input(f"MiniShell [{prompt_dir}]> ")
                self.execute(line)

            except KeyboardInterrupt:
                print("\nUse 'exit' to close the shell.")

            except EOFError:
                print("\nExiting Mini Shell.")
                self.running = False


if __name__ == "__main__":
    shell = MiniShell()
    shell.start()
