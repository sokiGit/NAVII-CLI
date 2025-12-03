import shutil

def shell_mv(args):
    if len(args) != 2:
        print("Usage: mv <source> <destination>")
        return 1

    source, destination = args
    try:
        shutil.move(source, destination)
        return 0
    except FileNotFoundError:
        print(f"Navii: mv: source '{source}' not found.")
        return 1
    except Exception as e:
        print(f"Navii: mv: error moving '{source}' to '{destination}': {e}")
        return 1