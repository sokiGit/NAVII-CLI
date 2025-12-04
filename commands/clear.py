import os

def shell_clear(args):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system("clear")
    return 0
