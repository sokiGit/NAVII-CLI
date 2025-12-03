import os

def shell_rm(args):
    if not args:
        print("Usage: rm <file_or_directory>")
        return 1

    return_code = 0
    for target in args:
        try:
            if os.path.isdir(target):
                os.rmdir(target)
            else:
                os.remove(target)
        except FileNotFoundError:
            print(f"Navii: rm: cannot remove '{target}': no such file or directory")
            return_code = 1
        except NotADirectoryError:
            print(f"Navii: rm: cannot remove '{target}': Not a directory (try file removal)")
            return_code = 1
        except OSError as e:
            if "Directory not empty" in str(e) or e.errno == 39:
                print(f"Navii: rm: cannot remove directory '{target}': Directory not empty (use 'rm -rf' equivalent for recursive removal)")
            else:
                print(f"Navii: rm: failed to remove '{target}': {e}")
            return_code = 1
        except Exception as e:
            print(f"Navii: rm: failed to remove '{target}': {e}")
            return_code = 1
    return return_code
