import sys

def shell_cat(args):
    if not args:
        print("Usage: cat <filename1> [filename2...]")
        return 1

    return_code = 0
    for filename in args:
        try:
            with open(filename, "r") as f:
                sys.stdout.write(f.read())
        except FileNotFoundError:
            print(f"Navii: cat: {filename}: No such file or directory")
            return_code = 1
        except IsADirectoryError:
            print(f"Navii: cat: {filename}: Is a directory")
            return_code = 1
        except Exception as e:
            print(f"Navii: cat: {filename}: Error reading file: {e}")
            return_code = 1
    return return_code