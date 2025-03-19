import os
import subprocess
import sys
import pty
from iassembly.interpreter import Interpreter
from iassembly.parser import Parser
from iassembly.lexer import Lexer
from iassembly.parser import ParseError
from iassembly.lexer import LexerError
from iassembly.interpreter import ValueError, InstructionError

# new instance of interpreter
interpreter = Interpreter()

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
    elif command == "iasm":
        try:
            
            if len(buffer) == 2 and os.path.splitext(buffer[1])[1] == ".iasm":
                
                with open(buffer[1], "r") as file:
                    code = file.read()
                    
                lexer = Lexer(code)
                token = lexer.scan_tokens()
                
                parser = Parser(token)
                ast = parser.parse()
            
                results = interpreter.interpret(ast)
                for result in results:
                    print(result)
                main_prompt()
            else:
                print("too many arguments while executing international-assembly")
        
        except ParseError as err:
            print(f"rules error : [{err}]")
        except LexerError as err:
            print(f"syntax error : [{err}]")
        except InstructionError as err:
            print(f"instruction error : [{err}]")
        except ValueError as err:
            print(f"value error : [{err}]")
        
    else:
        print(f"Command not recognized: {command}")
        main_prompt()

def main_prompt():
    where = os.getcwd()
    prompt = f"\033[1;35m[{where}]\033[1;33m | cyber=[{is_cyber_authenticated()}]\033[1;32m |\033[1;36m sudo=[True]\033[1;32m="
    
    try:
        command = input(prompt)
        buffer = shellx(command)
        process_command(buffer)
        main_prompt()
        
    except EOFError:
        print("\nExiting shell...")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nCommand interrupted")
        main_prompt()

if __name__ == "__main__":
    main_prompt()