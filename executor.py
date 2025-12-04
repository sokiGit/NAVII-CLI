import subprocess
import sys
import shlex
import os

def execute_shell_command(full_command_string):
    try:
        command_parts = shlex.split(full_command_string)
        if not command_parts:
            return 0


        if os.name == 'nt': 
            process = subprocess.run(
                full_command_string,
                check=False,
                shell=True,
                text=True,
                stdout=sys.stdout,
                stderr=sys.stderr,
               
            )
            return process.returncode
            
        else:
            try:
                process = subprocess.run(
                    command_parts,
                    check=False,
                    text=True,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                )
                return process.returncode
            
            except FileNotFoundError:
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

    return 0