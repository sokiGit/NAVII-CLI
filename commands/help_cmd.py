import pathlib

def shell_help(args):
    script_dir = pathlib.Path(__file__).resolve().parent if "__file__" in globals() else pathlib.Path.cwd()
    help_file_path = script_dir / "help_docs.txt"
    try:
        with open(help_file_path, "r") as f:
            print(f.read())
        return 0
    except FileNotFoundError:
        print(f"Navii: help: Error: help file not found at {help_file_path}.")
        return 1
    except Exception as e:
        print(f"Navii: help: An error occurred while reading the help file: {e}")
        return 1
