import os

def shell_mkdir(args):
    if not args:
        print("Usage: mkdir <directory_name>")
        return 1

    return_code = 0
    for dirname in args:
        try:
            os.makedirs(dirname)
        except FileExistsError:
            print(f"Navii: mkdir: cannot create directory '{dirname}': File exists")
            return_code = 1
        except PermissionError:
            print(f"Navii: mkdir: failed to create directory '{dirname}': Permission denied")
            return_code = 1
        except OSError as e:
            print(f"Navii: mkdir: failed to create directory '{dirname}': OS Error: {e}")
            return_code = 1
        except Exception as e:
            print(f"Navii: mkdir: failed to create directory '{dirname}': Error: {e}")
            return_code = 1
    return return_code
