import os
import shutil

def shell_cp(args):
    if len(args) != 2:
        print("Usage: cp <source> <destination>")
        return 1

    source, destination = args
    try:
        if os.path.isdir(source):
            print(f"Navii: cp: skipping directory '{source}': Recursive copy ('cp -r') is not implemented.")
            return 1
        else:
            shutil.copy(source, destination)
            return 0
    except FileNotFoundError:
        print(f"Navii: cp: source '{source}' not found.")
        return 1
    except IsADirectoryError:
        print(f"Navii: cp: target '{destination}' is a directory.")
        return 1
    except Exception as e:
        print(f"Navii: cp: error copying '{source}' to '{destination}': {e}")
        return 1