from iassembly.parser import *
from iassembly.buffer import *

class ExprVisitor:
        
    """
    Abstract visitor class for visiting expressions in the abstract syntax tree.
    Each visit method corresponds to a specific type of expression.
    """

    def accept(self, visitor):
        raise NotImplementedError("Subclasses must implement accept method")

    
class Interpreter(ExprVisitor):
    def __init__(self):
        self.environment = Environment()
        
    """
    Interpreter for evaluating expressions. Implements the visitor methods.
    """
    
    def visit_unknown_block(self, expr):
        self.execute_block(expr.block, Environment(self.environment))

    def execute_block(self, block, environment=None):
        previous = self.environment
        if environment is None:
                environment = Environment(previous)  # Lexical scoping
        self.environment = environment
        
        for statement in block:
            self.execute(statement)
        self.environment = previous
    
    def execute(self, stmt):
        return stmt.accept(self)
    
    def visit_bool_expr(self, expr):
        return (bool(expr.value), "bool", id(expr.value))
    
    def visit_char_expr(self, expr):
        return (expr.value, "char", id(expr.value))
    
    def visit_nil_expr(self, expr):
        return (None, "nil", None)
    
    def visit_int_expr(self, expr):
        return (int(expr.value), "int", id(expr.value))
    
    def visit_float_expr(self, expr):
        return (float(expr.value), "float", id(expr.value))
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)[0]
        right = self.evaluate(expr.right)[0]

        if expr.operator.lexeme == '+':
            _eval_ = left + right
            return (float(_eval_), "FLOAT", id(_eval_))
        elif expr.operator.lexeme == '-':
            _eval_ = left - right
            return (float(_eval_), "FLOAT", id(_eval_))
        elif expr.operator.lexeme == '*':
            _eval_ = left * right
            return (float(_eval_), "FLOAT", id(_eval_))
        elif expr.operator.lexeme == '/':
            _eval_ = left / right
            return (float(_eval_), "FLOAT", id(_eval_))
        elif expr.operator.lexeme == '>':
            _eval_ = left > right
            return (bool(_eval_), "BOOL", id(_eval_))
        elif expr.operator.lexeme == '>=':
            _eval_ = left >= right
            return (bool(_eval_), "BOOL", id(_eval_))
        elif expr.operator.lexeme == '<':
            _eval_ = left < right
            return (bool(_eval_), "BOOL", id(_eval_))
        elif expr.operator.lexeme == '==':
            _eval_ = left == right
            return (bool(_eval_), "BOOL", id(_eval_))
        elif expr.operator.lexeme == '===':
            _eval_ = type(left).__name__ == type(right).__name__
            return (bool(_eval_), "BOOL", id(_eval_))
        else:
            raise ValueError(f"Unsupported binary operator: {expr.operator}")

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)[0]
        right = self.evaluate(expr.right)[0]

        if expr.operator.lexeme == '&&':
            return left and right
        elif expr.operator.lexeme == '||':
            return left or right
        else:
            raise ValueError(f"Unsupported logical operator: {expr.operator}")

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)[0]

        if expr.operator.lexeme == '!':
            return not right
        else:
            raise ValueError(f"Unsupported unary operator: {expr.operator}")

    def visit_literal_expr(self, expr):
        return (str(expr.value), "str", id(expr.value))

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)
    
    def visit_using_type_expr(self, expr):
        return f"Type Id [{type(expr.value).__name__}]"
    

    def interpret(self, stmt):
        self.stmt = stmt
        if isinstance(self.stmt, list):  # Handle multiple statements
            results = []
            for expr in self.stmt:
                result = self.evaluate(expr)
                results.append(result)
            return results
        else:  # Handle a single statement
            return self.evaluate(self.stmt)

    def evaluate(self, expr):
        if expr is None:
            return None
        return expr.accept(self)