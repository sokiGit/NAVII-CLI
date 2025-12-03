import os
import shutil

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
