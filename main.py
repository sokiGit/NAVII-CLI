import os
import sys
import readline
import pathlib
import getpass

from utils.expands_vars import expand_vars_and_tilde
from utils.redirect import execute_navii_redirect
from utils.pipe import execute_navii_pipe
from executor import execute_shell_command
from Builtins import BUILTIN_COMMANDS


HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".navii_history")
MAX_HISTORY_SIZE = 1000

def main():
    os.system("clear")
    logo = """
  ____    ____  __ __   ____  ____ 
 |    \  /    ||  |  | |    ||    |
 |  _  ||  o  ||  |  |  |  |  |  | 
 |  |  ||     ||  |  |  |  |  |  | 
 |  |  ||  _  ||  :  |  |  |  |  | 
 |  |  ||  |  |\     /  |  |  |  | 
 |__|__||__|__| \ _ /  |____||____|
"""
    print(logo)

    try:
        readline.read_history_file(HISTORY_FILE)
    except:
        pass

    print("Welcome to Navii.")
    username = input("Enter your shell handle (e.g., miku): ").strip()
    if not username:
        try:
            username = getpass.getuser()
        except:
            username = "guest"

    print(f"Welcome home {username}")

    while True:
        try:
            current_path = os.getcwd()
            display_path = "/" if current_path == "/" else os.path.basename(current_path)
            prompt = f"{username}@Navii:{display_path}$ "

            user_input = input(prompt)
            if not user_input.strip():
                continue

            expanded = expand_vars_and_tilde(user_input)

            if ">" in expanded or "<" in expanded:
                execute_navii_redirect(expanded)
                continue

            if "|" in expanded:
                execute_navii_pipe(expanded)
                continue

            parts = expanded.split()
            command = parts[0]

            if command in BUILTIN_COMMANDS:
                BUILTIN_COMMANDS[command](parts[1:])
                continue

            execute_shell_command(expanded)

        except KeyboardInterrupt:
            print("\nInterrupted.")
        except EOFError:
            break

if __name__ == "__main__":
    main()