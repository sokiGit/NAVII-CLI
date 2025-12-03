import os

def shell_unset(args):
    if not args:
        print("Usage: unset <variable_name1> [variable_name2...]")
        return 1

    return_code = 0
    for key in args:
        if key in os.environ:
            try:
                del os.environ[key]
            except Exception as e:
                print(f"Navii: unset: failed to remove '{key}': {e}")
                return_code = 1
        else:
            print(f"Navii: unset: variable '{key}' not found.")
            return_code = 1
    return return_code
