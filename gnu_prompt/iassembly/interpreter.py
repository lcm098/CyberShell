from iassembly.parser import *
from iassembly.buffer import *
from iassembly.stdvar import StanderVariable

class ExprVisitor:
        
    """
    Abstract visitor class for visiting expressions in the abstract syntax tree.
    Each visit method corresponds to a specific type of expression.
    """

    def visit_number_expr(self, expr):
        raise NotImplementedError("visit_number_expr must be implemented by a subclass.")
    
    def visit_bool_expr(self, expr):
        raise NotImplementedError("visit_bool_expr must be implemented by a subclass.")
    
    def visit_nil_expr(self, expr):
        raise NotImplementedError("visit_nil_expr must be implemented by a subclass.")
    
    def visit_char_expr(self, expr):
        raise NotImplementedError("visit_char_expr must be implemented by a subclass.")
    
    def visit_binary_expr(self, expr):
        raise NotImplementedError("visit_binary_expr must be implemented by a subclass.")

    def visit_logical_expr(self, expr):
        raise NotImplementedError("visit_logical_expr must be implemented by a subclass.")

    def visit_unary_expr(self, expr):
        raise NotImplementedError("visit_unary_expr must be implemented by a subclass.")

    def visit_literal_expr(self, expr):
        raise NotImplementedError("visit_literal_expr must be implemented by a subclass.")

    def visit_grouping_expr(self, expr):
        raise NotImplementedError("visit_grouping_expr must be implemented by a subclass.")

    def visit_cmd_activation_expr(self, expr):
        raise NotImplementedError("visit_cmd_activation_expr must be implemented by a subclass.")


    def visit_using_type_expr(self, expr):
        raise NotImplementedError("visit_using_type_expr must be implemented by a subclass")

    def accept(self, visitor):
        raise NotImplementedError("Subclasses must implement accept method")

    def visit_unknown_block(self, stmt):
        raise NotImplementedError("visit_unknown_block must be implemented by a subclass")

    def visit_float_expr(self, expr):
        raise NotImplementedError("visit_float_expr must be implemented by a subclass")
    
    def visit_identifier(self, inst):
        raise NotImplementedError("visit_identifier must be implemented by a subclass")
        
    
    def visit_mov_instruction(self, inst):
        raise NotImplementedError("visit_mov_instruction must be implemented by a subclass")
    
    def accept(self, visitor):
        raise NotImplementedError("Subclasses must implement accept method")

class ValueError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
    def __repr__(self):
        return self.message
    
class InstructionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
    def __repr__(self):
        return self.message
    
class Interpreter(ExprVisitor):
    def __init__(self):
        self.environment = Environment()
        self.pointer_environment = PointerStructure()
    
    
    def visit_mov_instruction(self, inst):
        stander_variable = inst.stander_var.lexeme
        value = self.evaluate(inst.value)[0]
        
        stdvar = StanderVariable()
        
        if (stander_variable == stdvar.ras) or (stander_variable == stdvar.rbs) or (stander_variable == stdvar.rcs) or (stander_variable == stdvar.rds) or (stander_variable == stdvar.rex):
            if self.environment.is_defined(stander_variable):
                self.environment.assign(stander_variable, value)
            else:
                self.environment.define(stander_variable, value, False)
            
            if self.environment.is_defined(stdvar.rdo_var):
                self.environment.assign(stdvar.rdo_var, value)
            else:
                self.environment.define(stdvar.rdo_var, value, False)
        return (stander_variable, value)
        
    
    def visit_identifier(self, inst):
        identifier = inst.identifier.lexeme
        value = self.evaluate(identifier)
        return value
    
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