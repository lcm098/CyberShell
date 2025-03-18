import os
import subprocess
import sys
import pty

def is_cyber_authenticated():
    return False

def shellx(command):
    result = []
    current = ''
    in_quotes = False
    escape_next = False
    
    for char in command:
        if escape_next:
            current += char
            escape_next = False
        elif char == '\\':
            escape_next = True
        elif char == '"' or char == "'":
            in_quotes = not in_quotes
        elif char == ' ' and not in_quotes:
            if current:
                result.append(current)
                current = ''
        else:
            current += char
    
    if current:
        result.append(current)
    
    return result

def process_command(buffer):
    if not buffer:
        main_prompt()
        return
    
    command = buffer[0]
    
    if command == "-s":
        if len(buffer) < 2:
            print("Error: Missing command after -s")
            main_prompt()
            return
        
        cmd = buffer[1]
        args = buffer[2:]
        
        # Use pty for fully interactive commands
        try:
            # Create a pseudo-terminal and spawn the process
            command_list = [cmd] + args
            
            # Use pty.spawn without a custom read function
            pty.spawn(command_list)
            print(f"\nCommand completed")
        except Exception as e:
            print(f"Error: {e}")
        
        main_prompt()
    elif command == "exit":
        exit(0)
    else:
        print(f"Command not recognized: {command}")
        main_prompt()

def main_prompt():
    where = os.getcwd()
    prompt = f"[[{where}] | cyber=[{is_cyber_authenticated()}] | sudo=[True]= "
    
    try:
        command = input(prompt)
        buffer = shellx(command)
        process_command(buffer)
    except EOFError:
        print("\nExiting shell...")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nCommand interrupted")
        main_prompt()

if __name__ == "__main__":
    main_prompt()