import subprocess
import sys
import shlex
import os 

def shell_sudo(args):
    if not args:
        print("Usage: sudo <commands> [args..]")
        return 1

    quoted_args = " ".join(shlex.quote(a) for a in args)

    try:
        if os.name == 'nt':
            command_to_run = "runas /user:Administrator " + quoted_args
            
            try:
                process = subprocess.run(
                    command_to_run,
                    check=False,
                    shell=True, 
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    text=True,
                )
                return process.returncode
            except FileNotFoundError:
                print("Navii: External 'runas' program not found.")
                return 127
            
        else:
            command_to_run = "sudo " + quoted_args
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
                print("Navii: External 'sudo' program not found.")
                return 127
            
    except Exception as e:
        print(f"Navii sudo command execution error: {e}")
        return 1
    
    return 0