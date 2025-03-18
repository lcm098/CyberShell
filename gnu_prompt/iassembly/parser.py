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

    class CmdActivation:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Command(value={self.value})"
        
        def accept(self, visitor):
            return visitor.visit_cmd_activation_expr(self)
        
    class UsingType:
        def __init__(self, value):
            self.value = value
            
        def __repr__(self):
            return f"Using(value={self.value})"
        
        def accept(self, visitor):
            return visitor.visit_using_type_expr(self)
        
    class EmptyBlock:
        def __init__(self, block):
            self.block = block
        
        def __repr__(self):
            return f"Unknown_block(block={self.block})"
        
        def accept(self, visitor):
            return visitor.visit_unknown_block(self)
        
    class BITWISE_AND:
        def __init__(self, va1, va2):
            self.va1 = va1
            self.va2 = va2
        
        def __repr__(self):
            return f"BITWISE_AND(va1={self.va1, self.va2})"
        
        def accept(self, visitor):
            return visitor.visit_bitwise_and(self)
        
    class BITWISE_OR:
        def __init__(self, va1, va2):
            self.va1 = va1
            self.va2 = va2
        
        def __repr__(self):
            return f"BITWISE_OR(block={self.va1, self.va2})"
        
        def accept(self, visitor):
            return visitor.visit_bitwise_or(self)
        
    class BITWISE_NOT:
        def __init__(self, va1):
            self.va1 = va1
        
        def __repr__(self):
            return f"BITWISE_NOT(block={self.va1})"
        
        def accept(self, visitor):
            return visitor.visit_bitwise_not(self)
        
    class BITWISE_XOR:
        def __init__(self, va1, va2):
            self.va1 = va1
            self.va2 = va2
        
        def __repr__(self):
            return f"BITWISE_XOR(block={self.va1, self.va2})"
        
        def accept(self, visitor):
            return visitor.visit_bitwise_xor(self)
    
    
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
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements
 
    def declaration(self):
        if self.match(TokenType.LEFT_BRACE):
            return self.handle_unknown_block_statement()
        
        return self.expression()

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
        expr = self.unary()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    def primary(self):
        
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
            
        error_token = self.peek()
        self.error(error_token, "Expect expression.", self.current)

    def handle_unknown_block_statement(self):
        unknown_block = self.block()
        self.consume(TokenType.RIGHT_BRACE, "Expecting '}' after '{' (a unknown block statement)")
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