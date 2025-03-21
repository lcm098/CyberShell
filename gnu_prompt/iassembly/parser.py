from iassembly.lexer import *
from iassembly.interpreter import *

class Expr:
        
    class Binary:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right
        
        def __repr__(self):
            return f"Binary(left={self.left}, operator={self.operator}, right={self.right})"

        def accept(self, visitor):
            return visitor.visit_binary_expr(self)
        
    class Logical:
        def __init__(self, left, operator, right):
            self.left = left      # Left-hand side expression
            self.operator = operator  # Operator (AND/OR)
            self.right = right    # Right-hand side expression

        def accept(self, visitor):
            return visitor.visit_logical_expr(self)
        
    class Unary:
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right
        
        def __repr__(self):
            return f"Unary(operator={self.operator}, right={self.right})"
        
        def accept(self, visitor):
            return visitor.visit_unary_expr(self)

    class Literal:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Literal(value={self.value})"
        
        def accept(self, visitor):
            return visitor.visit_literal_expr(self)
        
        
    class INT:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Number(value={self.value})"
        
        def accept(self, visitor):
            return visitor.visit_int_expr(self)
        
    class FLOAT:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Number(value={self.value})"
        
        def accept(self, visitor):
            return visitor.visit_float_expr(self)
        
    class BOOL:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"BOOL(value={self.value})"
        
        def accept(self, visitor):
            return visitor.visit_bool_expr(self)

    class NIL:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Literal(value={None})"
        
        def accept(self, visitor):
            return visitor.visit_nil_expr(self)
        
    
    class CHAR:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Literal(value={self.value})"
        
        def accept(self, visitor):
            return visitor.visit_char_expr(self)
        
    class Grouping:
        def __init__(self, expression):
            self.expression = expression
        
        def __repr__(self):
            return f"Grouping(expression={self.expression})"
        
        def accept(self, visitor):
            return visitor.visit_grouping_expr(self)
        
    class UsingType:
        def __init__(self, value, line):
            self.value = value
            self.line = line
            
        def __repr__(self):
            return f"Using(value={self.value}, line={self.line})"
        
        def accept(self, visitor):
            return visitor.visit_using_type_expr(self)
        
    class EmptyBlock:
        def __init__(self, block):
            self.block = block
        
        def __repr__(self):
            return f"Unknown_block(block={self.block})"
        
        def accept(self, visitor):
            return visitor.visit_unknown_block(self)
        
        
    class MovInstruction:
        def __init__(self, opponent_x, opponent_y, line):
            self.opponent_x = opponent_x
            self.opponent_y = opponent_y
            self.line = line
        
        def __repr__(self):
            return f"mov instruction=({self.opponent_x}, {self.opponent_x}, {self.line})"
        
        def accept(self, visitor):
            return visitor.visit_mov_instruction(self)
        
    class Register:
        def __init__(self, register):
            self.register = register
        
        def __repr__(self):
            return f"Register(block={self.register})"
        
        def accept(self, visitor):
            return visitor.visit_register(self)
        
        
    class Identifier:
        def __init__(self, ident):
            self.identifier = ident
        
        def __repr__(self):
            return f"Register(block={self.identifier})"
        
        def accept(self, visitor):
            return visitor.visit_identifier(self)
        
    
class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
    def __repr__(self):
        return self.message

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        
        if self.match(TokenType.SECTION):
            self.consume(TokenType.DOT, "Expected '.' in the entry-point of text-code")
            self.consume(TokenType.TEXT, "Expected 'text' as the entry-point of code")
            self.consume(TokenType.DOUBLE_OR, "Expected '||' environment-encloser of main-text code")
            statements = []
                
            # Use peek instead of match to avoid consuming the end token prematurely
            while not self.match(TokenType.DOUBLE_OR):
                statements.append(self.declaration())

            return statements
        return []  # Return empty if no valid block is found
        
 
    def declaration(self):
        if self.match(TokenType.DOUBLE_OR):
            return self.handle_unknown_block_statement()
        
        elif self.match(TokenType.MOV):
            return self.handle_mov_instruction()
        
        elif self.match(TokenType.LOAD):
            # return self.handle_load_instruction()
            pass
        
        elif self.match(TokenType.CALL):
            # return self.handle_function_call()
            pass
        
        elif self.match(TokenType.COMPUTE):
            # return self.handle_compute_instruction()
            pass
        
        return self.expression()


    def handle_mov_instruction(self):
        line = self.peek().line
        opponent_x = self.expression()
        self.consume(TokenType.COMMA, "Expected ',' after mov x [mov x, y]")
        opponent_y = self.expression()
        return Expr.MovInstruction(opponent_x, opponent_y, line)
    
    
    def expression(self):
        return self.or_expr()
    
    def or_expr(self):
        expr = self.and_expr()
        while self.match(TokenType.CONDITIONAL_OR):
            operator = self.previous()
            right = self.and_expr()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def and_expr(self):
        expr = self.equality()
        while self.match(TokenType.CONDITIONAL_AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL, TokenType.DATA_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.MODULUS):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    def primary(self):
    
        if self.match(TokenType.EAX):
            return Expr.Register("eax")
        if self.match(TokenType.EBX):
            return Expr.Register("ebx")
        if self.match(TokenType.ECX):
            return Expr.Register("ecx")
        if self.match(TokenType.EDX):
            return Expr.Register("edx")
        if self.match(TokenType.EFX):
            return Expr.Register("efx")
        if self.match(TokenType.EXX):
            return Expr.Register("exx")
        if self.match(TokenType.EZX):
            return Expr.Register("ezx")
        
        if self.match(TokenType.INT):
            return Expr.INT(self.previous().literal)
        if self.match(TokenType.FLOAT):
            return Expr.FLOAT(self.previous().literal)
        if self.match(TokenType.FALSE):
            return Expr.BOOL('false')
        if self.match(TokenType.TRUE):
            return Expr.BOOL('true')
        if self.match(TokenType.NIL):
            return Expr.NIL('nil')
        if self.match(TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        if self.match(TokenType.CHAR):
            return Expr.CHAR(self.previous().literal)
            
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        
        if self.match(TokenType.IDENTIFIER):
            self.past(distance=1)
            ident = self.consume(TokenType.IDENTIFIER, "Expected an Identifier")
            return Expr.Identifier(ident)
            
        error_token = self.peek()
        self.error(error_token, "Expect expression.", self.current)

    def handle_unknown_block_statement(self):
        unknown_block = self.block()
        self.consume(TokenType.DOUBLE_OR, "Expecting '||' after '||' (a unknown block statement)")
        return Expr.EmptyBlock(unknown_block)
    
    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def match(self, *types):
        for token_type in types:
            current_type = self.peek().type
        
            if isinstance(current_type, tuple):
                current_type = current_type[0]
            
            if token_type == current_type:
                self.advance()
                return True    
        return False

    def check(self, token_type):
        if self.is_at_end():
            return False
        # Handle tuple comparison
        if isinstance(self.peek().type, tuple):
            return token_type in self.peek().type
        else:
            return self.peek().type == token_type

    def advance(self, distance=1):
        if not self.is_at_end():
            self.current += distance
        return self.previous()
    
    def past(self, distance=1):
        if not self.is_at_end():
            self.current -= distance
        return
    
    def future(self, distance=1):
        if not self.is_at_end():
            self.current += distance
        return

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self, distance=1):
        return self.tokens[self.current - distance]

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        self.error(self.peek(), message, self.peek().line)

    def error(self, token, message, line):
        
        previous_token = self.previous()
        advance_token = self.advance()
        
        raise ParseError(f"Error at = {previous_token.lexeme}, near at {token.lexeme}, advance= {advance_token.lexeme}: {message} : ***[line no.={line}]***")