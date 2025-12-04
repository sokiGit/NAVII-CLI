import subprocess
import sys
import shlex
import os 

def execute_navii_pipe(user_input):
    if user_input.count("|") != 1:
        print("Navii: Only single pipes are supported.")
        return 1

    left = user_input.split("|", 1)[0].strip()
    right = user_input.split("|", 1)[1].strip()

    try:
        if shlex.split(left)[0] in ["cd", "exit"] or shlex.split(right)[0] in ["cd", "exit"]:
            print("Navii: Cannot pipe state-changing commands ('cd', 'exit').")
            return 1
    except IndexError:
        print("Navii: Invalid pipe command format.")
        return 1
    
    try:
        process = subprocess.run(
            user_input,
            check=False,
            shell=True,
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
        
    except subprocess.TimeoutExpired:
        print("Navii: Pipe command timed out.")
        return 1
    except Exception as e:
        if isinstance(e, FileNotFoundError):
             shell_name = 'cmd.exe' if os.name == 'nt' else '/bin/sh'
             print(f"Navii: System shell ({shell_name}) or command not found. Cannot execute piped command.")
             return 127
        else:
            print(f"Navii piped command execution error: {e}")
            return 1