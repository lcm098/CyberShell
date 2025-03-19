import string
import os
import sys

# Define token types as constants
MOV = "MOV"
ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"
MOD = "MOD"
CMP = "CMP"
JMP = "JMP"
PUSH = "PUSH"
POP = "POP"
LOAD = "LOAD"
STORE = "STORE"
UNLOAD = "ULOAD"
UNSTORE = "USTORE"
FIPTR = "FIPTR"
INC = "INC"
GET = "GET"
DEC = "DEC"
LOOP = "LOOP"
COLON = "COLON"
COMMA = "COMMA"
DOT = "DOT"
LEFT_PAREN = "LEFT_PAREN"
RIGHT_PAREN = "RIGHT_PAREN"
LEFT_BRACE = "LEFT_BRACE"
RIGHT_BRACE = "RIGHT_BRACE"
LEFT_BRACKET = "LEFT_BRACKET"
RIGHT_BRACKET = "RIGHT_BRACKET"
SECTION = "SECTION"
CONDITIONAL_AND = "CONDITIONAL_AND"
BANG =  "BANG"
CONDITIONAL_OR = "CONDITIONAL_OR"
GLOBAL = "GLOBAL"
EXTERN = "EXTERN"
PUBLIC = "PUBLIC"
TEXT = "TEXT"
DATA = "DATA"
BSS = "BSS"
DOUBLE_OR = "DOUBLE_OR"
READ = "READ"
WRITE = "WRITE"
RETURN = "RETURN"
EXEC = "EXEC"
CALL = "CALL"
STRING = "STRING"
FLOAT = "FLOAT"
INT = "INT"
CHAR = "CHAR"
IDENTIFIER = "IDENTIFIER"
CMD_ACTIVATION = "CMD_ACTIVATION"
ADDRESS_OF_OPERATOR = "ADDRESS_OF_OPERATOR"
BANG_EQUAL = "BANG_EQUAL"
EQUAL_EQUAL = "EQUAL_EQUAL"
DATA_EQUAL = "DATA_EQUAL"
GREATER = "GREATER"
LESS = "LESS"
GREATER_EQUAL = "GREATER_EQUAL"
LESS_EQUAL = "LESS_EQUAL"
TRUE = "TRUE"
FALSE = "FALSE"
NIL = "NIL"
PUSHA = "PUSHA"
POPA = "POPA"
CLSV = "CLSV" # clear variable
LINK = "LINK"
IS = "IS"
ARRAY_GROUP_OPERATOR = "ARRAY_GROUP_OPERATOR"
INVOKE =  "INVOKE"
EOF = "EOF"  # Added missing EOF token type
SET = "SET"
INJECT = "INJECT"
HANT_OPERATOR = "HANT_OPERATOR"

TOKEN_TYPES = [
    MOV, ADD, SUB, MUL, DIV, MOD, CMP, JMP,
    CALL, PUSH, POP, LOAD, STORE, UNLOAD, UNSTORE,
    COLON, COMMA, DOT, LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE,
    RIGHT_BRACE, LEFT_BRACKET, RIGHT_BRACKET, SECTION, GLOBAL, EXTERN, PUBLIC,
    TEXT, DATA, BSS, DOUBLE_OR, READ, WRITE, RETURN, EXEC, FIPTR, INC, DEC, LOOP,
    ADDRESS_OF_OPERATOR, CONDITIONAL_AND, BANG, CONDITIONAL_OR, BANG_EQUAL, EQUAL_EQUAL,
    DATA_EQUAL, TRUE, FALSE, NIL, PUSHA, POPA, CLSV, LINK, IS, ARRAY_GROUP_OPERATOR,
    INVOKE, SET, GET, INJECT, HANT_OPERATOR
]

keywords = {
    "call" : CALL,
    "mov" : MOV,
    "fiptr" : FIPTR,
    "inject" : INJECT,
    "inc" : INC,
    "pusha" : PUSHA,
    "popa" : POPA,
    "clsv" : CLSV,
    "dec" : DEC,
    "get" : GET,
    "is" : IS,
    "link" : LINK,
    "true" : TRUE,
    "false" : FALSE,
    "nil" : NIL,
    "loop" : LOOP,
    "add" : ADD,
    "sub" : SUB,
    "mul" : MUL,
    "div" : DIV,
    "mod" : MOD,
    "cmp" : CMP,
    "jmp" : JMP,
    "invoke" : INVOKE,
    "set" : SET,
    
    "push" : PUSH,
    "pop" : POP,

    "load" : LOAD,
    "store" : STORE,
    "unload" : UNLOAD,
    "unstore" : UNSTORE,
    "section" : SECTION,
    "global" : GLOBAL,
    "extern" : EXTERN,
    "public" : PUBLIC,
    "text" : TEXT,
    "data" : DATA,
    "bss" : BSS,
    "read" : READ,
    "write" : WRITE,
    "return" : RETURN,
    "exec" : EXEC
}

class Token:
    def __init__(self, token_type, lexeme, line, literal=None):
        self.type = token_type
        self.lexeme = lexeme
        self.line = line
        self.literal = literal
    
    def __repr__(self):
        return f"Token(type={self.type}, lexeme={self.lexeme}, literal={self.literal}, line={self.line})"

class LexerError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __repr__(self):
        return self.message

class Lexer:
    def __init__(self, code_content):
        self.code_content = code_content
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def create_token(self, token_type, lexeme, line, literal=None):
        return Token(token_type, lexeme, line, literal)

    def report_error(self, line, message):
        raise LexerError(f"""lexer except {message}.\n\tOn Line=[{line}]""")

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(self.create_token(TokenType.EOF, "", self.line, None))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.code_content)

    def advance(self):
        self.current += 1
        return self.code_content[self.current - 1]

    def add_token(self, type, literal=None):
        text = self.code_content[self.start:self.current]
        self.tokens.append(self.create_token(type, text, self.line, literal))

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.code_content[self.current] != expected:
            return False
        self.advance()  # Move to the next character
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.code_content[self.current]

    def peek_next(self, distance=1):
        if self.current + distance >= len(self.code_content):
            return '\0'
        return self.code_content[self.current + distance]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.report_error(self.line, "Unterminated string.")
            return
        self.advance()  # The closing "
        value = self.code_content[self.start + 1:self.current - 1]
        self.add_token(STRING, value)

    def command_activation(self):
        while self.peek() != '\\' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.report_error(self.line, "Unterminated command literal.")
            return
        self.advance()  # The closing "
        value = self.code_content[self.start + 1:self.current - 1]
        self.add_token(CMD_ACTIVATION, value)
        
    def is_digit(self, c):
        return c.isdigit()

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
            value = float(self.code_content[self.start:self.current])
            self.add_token(FLOAT, value)
        else:
            # If no decimal point, treat it as an integer
            # Convert to int if no decimal found
            value = int(self.code_content[self.start:self.current])
            self.add_token(INT, value)

    def is_alpha(self, c):
        return c.isalpha() or c == '_'

    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self.code_content[self.start:self.current]
        type = keywords.get(text, IDENTIFIER)
        self.add_token(type)
        
    def char_consume(self):
        value = self.peek()
        self.add_token(CHAR, value)
        self.current += 1
        if not self.match('\''):
            self.report_error(self.line, "too many char in char literal")

    def scan_token(self):
        c = self.advance()
        
        if c == "|":
            if  self.match("|"):
                self.add_token(DOUBLE_OR)
            else:
                self.add_token(CONDITIONAL_OR)
        elif c == '@':
            self.add_token(ADDRESS_OF_OPERATOR)
        
        elif c == '#':
            self.add_token(HANT_OPERATOR)    
        
        elif c == "&":
            self.add_token(CONDITIONAL_AND)
        elif c == '(':
            self.add_token(LEFT_PAREN)
        elif c == ')':
            self.add_token(RIGHT_PAREN)
        elif c == '{':
            self.add_token(LEFT_BRACE)
        elif c == '}':
            self.add_token(RIGHT_BRACE)
        elif c == "[":
            self.add_token(LEFT_BRACKET)
        elif c == "]":
            self.add_token(RIGHT_BRACKET)
        elif c == ',':
            self.add_token(COMMA)
        elif c == '.':
            self.add_token(DOT)
        elif c == "%":
            self.add_token(MOD)
        elif c == '!':
            self.add_token(BANG_EQUAL if self.match('=') else BANG)
        elif c == '=':
            if self.match("="):
                if self.match("="):
                    self.add_token(DATA_EQUAL)
                else:
                    self.add_token(EQUAL_EQUAL)
        elif c == '<':
            if self.match("="):
                self.add_token(LESS_EQUAL)
            else:
                self.add_token(LESS)
        elif c == '>':
            self.add_token(GREATER_EQUAL if self.match('=') else GREATER)
        elif c == ':':
            self.add_token(COLON)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            
        elif c in {' ', '\r', '\t'}:
            pass  # Ignore whitespace
        elif c == '\n':
            self.line += 1
        elif c == '\\':
                self.command_activation()
        elif c == '"':
            if self.match('"'):
                if self.match('"'):
                    self.handle_multiline_comment()
                else:
                    self.report_error(self.line, "Expecting '\"' for multiline comment.")
            else:
                self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()
        elif c == "'":
            self.char_consume()
        else:
            self.report_error(self.line, "Unexpected character.")
            
    def handle_multiline_comment(self):
        # Start by advancing three times to skip the initial """
        self.advance()  # Skip the first "
        self.advance()  # Skip the second "
        self.advance()  # Skip the third "

        while not self.is_at_end():
            if self.peek() == '"' and self.peek_next() == '"' and self.peek_next(2) == '"':
                self.advance()  # Skip the first "
                self.advance()  # Skip the second "
                self.advance()  # Skip the third "
                return  # Successfully found the end of the comment
            if self.peek() == '\n':
                self.line += 1  # Increment the line count if a newline is encountered
            self.advance()  # Continue advancing through the comment

        # If the end of the file is reached without finding the end of the comment
        self.report_error(self.line, "Unterminated multiline comment.")

class TokenType:
    # Define token types as constants
    MOV = "MOV"
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    CMP = "CMP"
    JMP = "JMP"
    PUSH = "PUSH"
    POP = "POP"
    LOAD = "LOAD"
    STORE = "STORE"
    UNLOAD = "ULOAD"
    UNSTORE = "USTORE"
    FIPTR = "FIPTR"
    INC = "INC"
    GET = "GET"
    DEC = "DEC"
    LOOP = "LOOP"
    COLON = "COLON"
    COMMA = "COMMA"
    DOT = "DOT"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    SECTION = "SECTION"
    CONDITIONAL_AND = "CONDITIONAL_AND"
    BANG =  "BANG"
    CONDITIONAL_OR = "CONDITIONAL_OR"
    GLOBAL = "GLOBAL"
    EXTERN = "EXTERN"
    PUBLIC = "PUBLIC"
    TEXT = "TEXT"
    DATA = "DATA"
    BSS = "BSS"
    DOUBLE_OR = "DOUBLE_OR"
    READ = "READ"
    WRITE = "WRITE"
    RETURN = "RETURN"
    EXEC = "EXEC"
    CALL = "CALL"
    STRING = "STRING"
    FLOAT = "FLOAT"
    INT = "INT"
    CHAR = "CHAR"
    IDENTIFIER = "IDENTIFIER"
    CMD_ACTIVATION = "CMD_ACTIVATION"
    ADDRESS_OF_OPERATOR = "ADDRESS_OF_OPERATOR"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    DATA_EQUAL = "DATA_EQUAL"
    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NIL = "NIL"
    PUSHA = "PUSHA"
    POPA = "POPA"
    CLSV = "CLSV" # clear variable
    LINK = "LINK"
    IS = "IS"
    ARRAY_GROUP_OPERATOR = "ARRAY_GROUP_OPERATOR"
    INVOKE =  "INVOKE"
    EOF = "EOF"  # Added missing EOF token type
    SET = "SET"
    INJECT = "INJECT"
    HANT_OPERATOR = "HANT_OPERATOR"