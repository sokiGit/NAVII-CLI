import os

def shell_touch(args):
    if not args:
        print("Usage: touch <filename1> [filename2...]")
        return 1

    return_code = 0
    for filename in args:
        try:
            with open(filename, "a"):
                os.utime(filename, None)
        except Exception as e:
            print(f"Navii: touch: cannot touch '{filename}': {e}")
            return_code = 1
    return return_code