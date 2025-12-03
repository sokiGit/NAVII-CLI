
import os
import sys
import shlex
import subprocess
import shutil
import pathlib
import readline
import getpass

HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".navii_history")
MAX_HISTORY_SIZE = 1000

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

def shell_echo(args):
    print(" ".join(args))
    return 0

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

def shell_ls(args):
    target_dir = args[0] if args else os.getcwd()
    if os.path.isfile(target_dir):
        print(target_dir)
        return 0

    try:
        items = os.listdir(target_dir)
        display_items = sorted({item for item in items if not item.startswith('.')})

        if not display_items:
            return 0

        terminal_width = shutil.get_terminal_size((80, 20)).columns
        max_len = max(len(item) for item in display_items)
        column_width = max_len + 2
        num_columns = max(1, terminal_width // column_width)
        num_items = len(display_items)
        num_rows = (num_items + num_columns - 1) // num_columns

        for row in range(num_rows):
            line = []
            for col in range(num_columns):
                index = row + col * num_rows
                if index < num_items:
                    item = display_items[index]
                    line.append(item.ljust(column_width))
            print("".join(line))

        return 0

    except FileNotFoundError:
        print(f"Navii: ls: cannot access '{target_dir}': No such file or directory")
        return 1
    except NotADirectoryError:
        print(f"Navii: ls: cannot access '{target_dir}': Not a directory")
        return 1
    except PermissionError:
        print(f"Navii: ls: cannot access '{target_dir}': Permission denied")
        return 1
    except Exception as e:
        print(f"Navii: ls: an unexpected error occurred: {e}")
        return 1

def shell_clear(args):
    os.system("clear")
    return 0

def shell_pwd(args):
    print(os.getcwd())
    return 0

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

def shell_help(args):
    script_dir = pathlib.Path(__file__).resolve().parent if "__file__" in globals() else pathlib.Path.cwd()
    help_file_path = script_dir / "help_docs.txt"
    try:
        with open(help_file_path, "r") as f:
            print(f.read())
        return 0
    except FileNotFoundError:
        print(f"Navii: help: Error: help file not found at {help_file_path}.")
        return 1
    except Exception as e:
        print(f"Navii: help: An error occurred while reading the help file: {e}")
        return 1

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

def shell_sudo(args):
    if not args:
        print("Usage: sudo <commands> [args..]")
        return 1

    quoted = " ".join(shlex.quote(a) for a in args)
    command_to_run = "sudo " + quoted
    try:
        process = subprocess.run(
            command_to_run,
            check=False,
            shell=True,
            executable="/bin/sh",
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
        )
        return process.returncode
    except FileNotFoundError:
        print("Navii: External 'sudo' program not found:")
        return 127
    except Exception as e:
        print(f"Navii sudo command execution error: {e}")
        return 1

BUILTIN_COMMANDS = {
    "cat": shell_cat,
    "cd": shell_cd,
    "clear": shell_clear,
    "cp": shell_cp,
    "mv": shell_mv,
    "exit": sys.exit,
    "echo": shell_echo,
    "help": shell_help,
    "ls": shell_ls,
    "mkdir": shell_mkdir,
    "pwd": shell_pwd,
    "rm": shell_rm,
    "sudo": shell_sudo,
    "unset": shell_unset,
    "export": shell_export,
    "touch": shell_touch,
}


def expand_vars_and_tilde(command_string):
    if not command_string:
        return command_string

    result = []
    i = 0
    length = len(command_string)
    in_single = False
    in_double = False

    def expand_var_name(name):
        return os.environ.get(name, "")

    while i < length:
        ch = command_string[i]

        if ch == "\\":
            if i + 1 < length:
                result.append(command_string[i + 1])
                i += 2
                continue
            else:
                result.append("\\")
                i += 1
                continue

        if ch == "'" and not in_double:
            in_single = not in_single
            result.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            result.append(ch)
            i += 1
            continue

        if ch == "~" and not in_single and not in_double:
            prev_char = command_string[i - 1] if i > 0 else None
            if prev_char is None or prev_char.isspace():
                if i + 1 == length or command_string[i + 1] == "/" or command_string[i + 1].isspace():
                    result.append(os.path.expanduser("~"))
                    i += 1
                    continue
            result.append("~")
            i += 1
            continue

        if ch == "$" and not in_single:
            if i + 1 >= length:
                result.append("$")
                i += 1
                continue

            if command_string[i + 1] == "{":
                j = i + 2
                var_name_chars = []
                while j < length and command_string[j] != "}":
                    var_name_chars.append(command_string[j])
                    j += 1
                if j < length and command_string[j] == "}":
                    var_name = "".join(var_name_chars)
                    result.append(expand_var_name(var_name))
                    i = j + 1
                    continue
                else:
                    result.append("${")
                    i += 2
                    continue
            else:
                j = i + 1
                var_name_chars = []
                while j < length and (command_string[j].isalnum() or command_string[j] == "_"):
                    var_name_chars.append(command_string[j])
                    j += 1
                if var_name_chars:
                    var_name = "".join(var_name_chars)
                    result.append(expand_var_name(var_name))
                    i = j
                    continue
                else:
                    result.append("$")
                    i += 1
                    continue

        result.append(ch)
        i += 1

    return "".join(result)


def execute_shell_command(full_command_string):
    try:
        command_parts = shlex.split(full_command_string)
        if not command_parts:
            return 0

        process = subprocess.run(
            command_parts,
            check=False,
            text=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        return process.returncode
    except FileNotFoundError:
        try:
            process = subprocess.run(
                full_command_string,
                check=False,
                shell=True,
                executable="/bin/sh",
                stdout=sys.stdout,
                stderr=sys.stderr,
                text=True,
            )
            return process.returncode
        except FileNotFoundError:
            print(f"Navii: Command not found: {full_command_string.split()[0]}")
            return 127
    except Exception as e:
        print(f"Navii shell execution error: {e}")
        return 1

def execute_navii_redirect(user_input):
    if user_input.count(">") > 1 or user_input.count("<") > 1:
        print("Navii: Only single output (>) or input (<) redirection is supported.")
        return 1

    if "|" in user_input and (">" in user_input or "<" in user_input):
        print("Navii: Cannot combine pipes and redirection in a single command yet.")
        return 1

    first_token = user_input.split()[0] if user_input.split() else ""
    if first_token in ["cd", "exit"]:
        print(f"Navii: Command '{first_token}' is state-changing and cannot be redirected.")
        return 1

    try:
        process = subprocess.run(
            user_input,
            check=False,
            shell=True,
            executable="/bin/sh",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        if process.stdout:
            sys.stdout.write(process.stdout)
        if process.stderr:
            sys.stderr.write(f"Redirection Error: {process.stderr}")
        return process.returncode
    except FileNotFoundError:
        print("Navii: System shell (/bin/sh) not found. Cannot execute redirected command.")
        return 127
    except subprocess.TimeoutExpired:
        print("Navii: Redirected command timed out.")
        return 1
    except Exception as e:
        print(f"Navii redirection execution error: {e}")
        return 1

def execute_navii_pipe(user_input):
    if user_input.count("|") != 1:
        print("Navii: Only single pipes are supported.")
        return 1

    left = user_input.split("|", 1)[0].strip()
    right = user_input.split("|", 1)[1].strip()

    if left.split()[0] in ["cd", "exit"] or right.split()[0] in ["cd", "exit"]:
        print("Navii: Cannot pipe state-changing commands ('cd', 'exit').")
        return 1

    try:
        process = subprocess.run(
            user_input,
            check=False,
            shell=True,
            executable="/bin/sh",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
        )
        if process.stdout:
            sys.stdout.write(process.stdout)
        if process.stderr:
            sys.stderr.write(f"Pipe Error: {process.stderr}")
        return process.returncode
    except FileNotFoundError:
        print("Navii: System shell (/bin/sh) not found. Cannot execute piped command.")
        return 127
    except subprocess.TimeoutExpired:
        print("Navii: Pipe command timed out.")
        return 1
    except Exception as e:
        print(f"Navii piped command execution error: {e}")
        return 1

def main():
    os.system("clear")
    logo = """
  ____    ____  __ __   ____  ____ 
 |    \  /    ||  |  | |    ||    |
 |  _  ||  o  ||  |  |  |  |  |  | 
 |  |  ||     ||  |  |  |  |  |  | 
 |  |  ||  _  ||  :  |  |  |  |  | 
 |  |  ||  |  |\     /  |  |  |  | 
 |__|__||__|__| \ _ /  |____||____|
"""
    print(logo)

    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass
    except Exception:
        pass

    readline.set_history_length(MAX_HISTORY_SIZE)

    print("Welcome to Navii.")
    username = input("Enter your shell handle (e.g., miku): ").strip()
    if not username:
        try:
            username = getpass.getuser()
        except Exception:
            username = "guest"

    print(f"Welcome home {username}")
    print("Type 'exit' to quit. Pipes (|), Redirection (>, <), external functions, expanded input, unset and sudo are now supported. Type 'help' for command and function list.")

    while True:
        try:
            current_path = os.getcwd()
            display_path = "/" if current_path == "/" else os.path.basename(current_path)

            prompt = f"{username}@Navii:{display_path}$ "
            user_input = input(prompt)

            if not user_input.strip():
                continue

            expanded_input = expand_vars_and_tilde(user_input)

            if ">" in expanded_input or "<" in expanded_input:
                execute_navii_redirect(expanded_input)
                continue

            if "|" in expanded_input:
                execute_navii_pipe(expanded_input)
                continue

            try:
                parts = shlex.split(expanded_input)
            except ValueError:
                print("Navii: Invalid command quoting or syntax.")
                continue

            if not parts:
                continue

            command = parts[0]

            if command in BUILTIN_COMMANDS:
                if command == "exit":
                    try:
                        readline.write_history_file(HISTORY_FILE)
                    except Exception as e:
                        print(f"Navii: Error writing history file: {e}")

                    print("Exiting Navii...")
                    if len(parts) > 1:
                        try:
                            code = int(parts[1])
                        except Exception:
                            code = 0
                        sys.exit(code)
                    else:
                        sys.exit(0)
                elif command == "cd":
                    rc = BUILTIN_COMMANDS[command](parts[1:])
                else:
                    rc = BUILTIN_COMMANDS[command](parts[1:])
                continue

            execute_shell_command(expanded_input)

        except KeyboardInterrupt:
            print("\nNavii: Operation interrupted.")
        except EOFError:
            try:
                readline.write_history_file(HISTORY_FILE)
            except Exception as e:
                print(f"Navii: Error writing history file: {e}")
            print("\nExiting Navii...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
