from iassembly.parser import *
from iassembly.buffer import *
from iassembly.stdlib import *

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
        
    def visit_Hidden_list_creation(self, inst):
        raise NotImplementedError("visit_Hidden_list_creation must be implemented by a subclass")
    
    def visit_Load_instruction(self, inst):
        raise NotImplementedError("visit_Load_instruction must be implemented by a subclass")
    
    def visit_mov_instruction(self, inst):
        raise NotImplementedError("visit_mov_instruction must be implemented by a subclass")
    
    def accept(self, visitor):
        raise NotImplementedError("Subclasses must implement accept method")

    def visit_System_function_call(self, inst):
        raise NotImplementedError("visit_System_function_call must implement as a method")

    def visit_Compute_instruction_call(self, inst):
        raise NotImplementedError("visit_Compute_instruction_call must be implemented by a subclass")

    def visit_register(self, expr):
        raise NotImplementedError("visit_register must be implemented by a subclass")


class NotImplementedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
    def __repr__(self):
        return self.message

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
        self.StanderLib = StanderLibrary()
        
    def visit_identifier(self, expr):
        return (expr.identifier.lexeme, "identifier", id(expr.identifier))
        
    def visit_register(self, expr):
        return (expr.register, "register", id(expr.register))
    
    def visit_call_pointer_list(self, expr):
        return (expr.pointer, "fptr", id(expr.pointer))
    
    def visit_value_pointer_list(self, expr):
        return (expr.pointer, "vptr", id(expr.pointer))
    
    def visit_compare_pointer_list(self, expr):
        return (expr.pointer, "cptr", id(expr.pointer))
    
    def visit_make_hidden_list(self, expr):
        elements = expr.elements
        line = expr.line
        
        clean_list = []
        for item in elements:
            clean_list.append(self.is_opponent_y_regis(self.evaluate(item), line))
        
        return clean_list
    
    def visit_load_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if opponent_x[1] == "register":
            self.push_in_environment(opponent_x, list(self.is_opponent_y_regis(opponent_y, line)))
        else:
            raise InstructionError(f"identifier {opponent_x} is not a 'register' type. \n\tOn Line=[{line}]")
        
    def visit_call_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if opponent_y[1] == "fptr":
            while not isinstance(opponent_y, list):
                opponent_y = self.environment.get(opponent_y)

            clean_list = []
            for item in opponent_y:
                clean_list.append(item[0])
            
            if opponent_x[1] == "identifier" and isinstance(opponent_y, list):
                if self.StanderLib.check_right_system_function(opponent_x[0]):
                    self.StanderLib.call_impropriated_function(opponent_x[0], clean_list)
                else:
                    raise InstructionError(f"Not impropriated function {opponent_y}. \n\tOn Line=[{line}]")
            else:
                raise InstructionError(f"miss use at function call of {opponent_x} and {opponent_y}. \n\tOn Line=[{line}]")
        else:
            raise InstructionError(f"opponent_y -> {opponent_y} is not a v(ptr)Type. \n\tOn Line={line}")
    
    def visit_compute_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if opponent_x[1] == "vptr":
            value = self.evaluate(opponent_y)
            return value
        else:
            raise InstructionError(f"Unable to store value in {opponent_x}, use opponent 'v(Register)Type'. \n\tOn Line=[{line}]")
    
    def visit_link_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if opponent_y[1] in ("register"):
            clean_list = self.environment.get(opponent_y)
            
            if opponent_x[1] in ("vptr", "fptr", "cptr") and isinstance(clean_list, list):
                self.push_in_environment(opponent_x, opponent_y)
            else:
                raise InstructionError(f"Unable to store value {clean_list} in {opponent_x}, use opponent 'v(Register)Type'. \n\tOn Line=[{line}]")
        
        elif opponent_y[1] in ("vptr", "fptr", "cptr"):
            
            while not isinstance(opponent_y, list):
                opponent_y = self.environment.get(opponent_y)
                
            if opponent_x[1] in ("register") and isinstance(clean_list, list):
                self.push_in_environment(opponent_x, opponent_y)
                print(opponent_x, opponent_y)
            else:
                raise InstructionError(f"Unable to store value {clean_list} in {opponent_x}, use opponent 'e(Register)Type'. \n\tOn Line=[{line}]")
        else:
            raise InstructionError(f"opponent_y expected as (e)Type or (v)Type register but, i got {opponent_y}")

            
        
    def visit_mov_instruction(self, inst):
        
        try:
            line = inst.line
            opponent_x = self.evaluate(inst.opponent_x)
            opponent_y = self.evaluate(inst.opponent_y)

            if isinstance(opponent_y, list):
                self.push_in_environment(opponent_x, opponent_y)
            else:    
                self.push_in_environment(opponent_x, self.is_opponent_y_regis(opponent_y, line))
            
        except Exception as err:
            raise InstructionError(str(err)+f"\n\tOn Line=[{line}]")
        
    def is_opponent_y_regis(self, y, line):
        
        if y[1] in ("register", "identifier"):
            if self.environment.is_defined(y):
                value = self.environment.get(y)
                if y[1] in ("register", "identifier"):
                    return self.is_opponent_y_regis(value, line)
                else:
                    return value
            else:
                raise InstructionError(f"using of {y} without initialing it, before.")
        else:
            return y
            
    
    def push_in_environment(self, x, y, is_const=False):
        
        if self.environment.is_defined(x):
            self.environment.assign(x, y)
        else:
            self.environment.define(x, y, is_const)
            
        
    def is_list(self, item):
        
        if isinstance(item, list):
            return True
        else:
            return False
        
    def calculate_identifier(self, inst):
        identifier = inst.identifier.lexeme
        line = inst.line
        if self.environment.is_defined(identifier):
            value = self.environment.get(identifier)
            return value
        else:
            raise InstructionError(f"identifier {identifier} is not defined, while using it. \t\tOn Line =[{line}]")
    
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
            return (float(_eval_), "float", id(_eval_))
        elif expr.operator.lexeme == '-':
            _eval_ = left - right
            return (float(_eval_), "float", id(_eval_))
        elif expr.operator.lexeme == '*':
            _eval_ = left * right
            return (float(_eval_), "float", id(_eval_))
        elif expr.operator.lexeme == '/':
            _eval_ = left / right
            return (float(_eval_), "float", id(_eval_))
        elif expr.operator.lexeme == '%':
            _eval_ = left % right
            return (float(_eval_), "float", id(_eval_))
        elif expr.operator.lexeme == '>':
            _eval_ = left > right
            return (bool(_eval_), "bool", id(_eval_))
        elif expr.operator.lexeme == '>=':
            _eval_ = left >= right
            return (bool(_eval_), "bool", id(_eval_))
        elif expr.operator.lexeme == '<':
            _eval_ = left < right
            return (bool(_eval_), "bool", id(_eval_))
        elif expr.operator.lexeme == "!=":
            _eval_ = left != right
            return (bool(_eval_), "bool", id(_eval_))
        elif expr.operator.lexeme == '==':
            _eval_ = str(left) == str(right)
            return (bool(_eval_), "bool", id(_eval_))
        elif expr.operator.lexeme == '===':
            _eval_ = ((type(left).__name__ == type(right).__name__) and (left == right))
            return (bool(_eval_), "bool", id(_eval_))
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