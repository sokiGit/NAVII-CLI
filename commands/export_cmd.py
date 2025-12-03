import os

def shell_export(args):
    if not args:
        for key, value in sorted(os.environ.items()):
            print(f'declare -x {key}="{value}"')
        return 0

    return_code = 0
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            try:
                os.environ[key] = value
            except Exception as e:
                print(f"Navii: export: failed to set '{arg}': {e}")
                return_code = 1
        else:
            if arg in os.environ:
                print(f'declare -x {arg}="{os.environ[arg]}"')
            else:
                print(f"Navii: export: {arg}: not found")
                return_code = 1
    return return_code
