import os

def shell_cd(args):
    if not args:
        print("Usage: cd <directory>")
        return 1

    target = args[0]
    try:
        os.chdir(target)
        return 0
    except FileNotFoundError:
        print(f"Navii: Directory not found: {target}")
        return 1
    except Exception as e:
        print(f"Navii: Error changing directory: {e}")
        return 1