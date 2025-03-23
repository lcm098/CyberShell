from iassembly.parser import *
from iassembly.buffer import *
from iassembly.stdlib import *
from iassembly.environment import environment

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
        self.environment = environment
        self.StanderLib = StanderLibrary()
        self.persistent_values = {}  # Store for persistent registers
        
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
    
    def visit_const_register(self, expr):
        # Return const register with its type
        return (expr.const, "const", id(expr.const))
    
    def visit_persistent_register(self, expr):
        # Return persistent register with its type
        return (expr.persis, "persistent", id(expr.persis))
    
    def visit_rptr_pointer(self, expr):
        return (expr.pointer, "rptr", id(expr.pointer))
    
    def visit_make_hidden_list(self, expr):
        elements = expr.elements
        line = expr.line
        
        clean_list = []
        for item in elements:
            clean_list.append(self.is_opponent_y_regis(self.evaluate(item), line))
        
        return clean_list
    
    def visit_list_element_access(self, expr):
        name = self.evaluate(expr.name)
        index = self.evaluate(expr.index)
        line = expr.line
        
        if self.environment.is_defined(name):
            fetched = self.environment.get(name)
            
            # Check if fetched is a list and index is valid
            if isinstance(fetched, list):
                # Extract index value if it's a tuple (like your other values)
                if isinstance(index, tuple) and len(index) >= 1:
                    index_value = index[0]
                else:
                    index_value = index
                    
                # Validate index
                if isinstance(index_value, int) and 0 <= index_value < len(fetched):
                    return fetched[index_value]
                else:
                    raise InstructionError(f"Invalid index {index_value} for list {name}. \n\tOn Line=[{line}]")
            else:
                raise InstructionError(f"{name} is not a list, cannot access element. \n\tOn Line=[{line}]")
        else:
            raise InstructionError(f"List {name} is not defined. \n\tOn Line=[{line}]")
    
    
    def visit_load_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if opponent_x[1] in ("register") and opponent_y[1] in ("vptr", "cptr", "fptr", "rptr"):
            y_value = self.environment.get(opponent_y)
            self.push_in_environment(opponent_x, y_value)
            
        else:
            raise InstructionError(f"invalid load x, y combination, where x should be (eTypeRegister) and y should be(v,c,f,r)TypeRegister only. \n\tOn Line =[{line}]")
        pass
        
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
                    
                    return_value = self.StanderLib.call_impropriated_function(opponent_x[0], clean_list)
                    self.push_in_environment(("rptr", "rptr", id("rptr")), return_value)
                    
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
            self.push_in_environment(opponent_x, opponent_y)
        else:
            raise InstructionError(f"Unable to store value in {opponent_x}, use opponent 'v(Register)Type'. \n\tOn Line=[{line}]")
    
    def visit_link_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if opponent_y[1] in ("register"):
            if opponent_x[1] in ("vptr", "fptr", "cptr"):
                y_value = self.environment.get(opponent_y)
                self.push_in_environment(opponent_x, y_value)
            else:
                raise InstructionError(f"Unable to store value {opponent_y} in {opponent_x}, use opponent 'v(Register)Type'. \n\tOn Line=[{line}]")
        
        elif opponent_y[1] in ("vptr", "fptr", "cptr"):
            if opponent_x[1] in ("register"):
                y_value = self.environment.get(opponent_y)
                self.push_in_environment(opponent_x, y_value)
            else:
                raise InstructionError(f"Unable to store value {opponent_y} in {opponent_x}, use opponent 'e(Register)Type'. \n\tOn Line=[{line}]")
        else:
            raise InstructionError(f"opponent_y expected as (e)Type or (v)Type register but, i got {opponent_y}")
            
    def visit_mov_instruction(self, inst):
        try:
            line = inst.line
            opponent_x = self.evaluate(inst.opponent_x)
            opponent_y = self.evaluate(inst.opponent_y)
            
            # Handle const registers - prevent modification after initialization
            if opponent_x[1] == "const":
                if self.environment.is_defined(opponent_x):
                    raise InstructionError(f"Cannot modify constant register {opponent_x[0]}. \n\tOn Line=[{line}]")
                else:
                    # First initialization of a constant register
                    if isinstance(opponent_y, list):
                        clean_list = self.make_clean_list(opponent_y)
                        self.push_in_environment(opponent_x, clean_list, is_const=True)
                    else:
                        self.push_in_environment(opponent_x, self.is_opponent_y_regis(opponent_y, line), is_const=True)
                    return
            
            # Handle persistent registers - accumulate values
            if opponent_x[1] == "persistent":
                persistent_id = opponent_x[0]
                
                if isinstance(opponent_y, list):
                    clean_list = self.make_clean_list(opponent_y)
                    # Check if we should accumulate or replace
                    if self.environment.has_persistent(persistent_id):
                        old_value = self.environment.get_persistent(persistent_id)
                        # Accumulate if numeric
                        if isinstance(old_value, list) and len(old_value) > 0 and isinstance(old_value[0][0], (int, float)) and \
                           isinstance(clean_list[0][0], (int, float)):
                            # Create proper value tuple preserving the format
                            result_value = old_value[0][0] + clean_list[0][0]
                            result_type = "int" if isinstance(result_value, int) else "float"
                            clean_list = [(result_value, result_type, id(result_value))]
                    
                    self.environment.store_persistent(persistent_id, clean_list)
                    self.push_in_environment(opponent_x, clean_list)
                else:
                    value = self.is_opponent_y_regis(opponent_y, line)
                    # Check if we should accumulate or replace
                    if self.environment.has_persistent(persistent_id):
                        old_value = self.environment.get_persistent(persistent_id)
                        if isinstance(old_value[0], (int, float)) and isinstance(value[0], (int, float)):
                            # Create proper value tuple preserving the format
                            result_value = old_value[0] + value[0]
                            result_type = "int" if isinstance(result_value, int) else "float"
                            value = (result_value, result_type, id(result_value))
                    
                    self.environment.store_persistent(persistent_id, value)
                    self.push_in_environment(opponent_x, value)
                return
            
            # Standard register handling
            if opponent_x[1] == "register":
                if isinstance(opponent_y, list):
                    clean_list = self.make_clean_list(opponent_y)
                    self.push_in_environment(opponent_x, clean_list)
                else:
                    value = self.is_opponent_y_regis(opponent_y, line)
                    # If value is a list, handle it properly
                    if isinstance(value, list):
                        self.push_in_environment(opponent_x, value)
                    else:
                        self.push_in_environment(opponent_x, value)
                        
        except Exception as err:
            raise InstructionError(str(err)+f"\n\tOn Line=[{line}]")
        
    def make_clean_list(self, lst):
        clean = []
        for item in lst:
            if item[1] in ("register", "vptr", "cptr", "fptr", "identifier", "const", "persistent"):
                value = self.environment.get(item)
                if isinstance(value, list):
                    clean.append(self.make_clean_list(value))
                else:
                    clean.append(value)
            else:
                clean.append(item)
        return clean
        
    def is_opponent_y_regis(self, y, line):
        if y[1] in ("register", "identifier", "const", "persistent"):
            if self.environment.is_defined(y):
                value = self.environment.get(y)
                # Check if the value is a list or another register reference
                if isinstance(value, list):
                    return value  # Return the list directly
                elif y[1] in ("register", "identifier", "const", "persistent"):
                    return self.is_opponent_y_regis(value, line)
                else:
                    return value
            else:
                # Special handling for persistent registers that might exist in persistent store
                if y[1] == "persistent" and y[0] in self.persistent_values:
                    return self.persistent_values[y[0]]
                raise InstructionError(f"using of {y} without initialing it, before.")
        else:
            return y
            
    def push_in_environment(self, x, y, is_const=False):
        if x[1] == "const":
            is_const = True
            
        if self.environment.is_defined(x):
            # Prevent reassigning to const registers
            if self.environment.is_const(x):
                raise InstructionError(f"Cannot reassign constant register {x[0]}")
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
    
        if expr.value.capitalize() == "True":
            boolean_value = True
        elif expr.value.capitalize() == "False":
            boolean_value = False
        else:
            raise ValueError(f"Invalid boolean value: {expr.value}")
        return (boolean_value, "bool", id(boolean_value))
    
    
    def visit_char_expr(self, expr):
        return (expr.value, "char", id(expr.value))
    
    def visit_none_expr(self, expr):
        return (None, "None", None)
    
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
            
            _eval_ = left == right
            return (bool(_eval_), "bool", id(_eval_))
        elif expr.operator.lexeme == '===':
            _eval_ = ((type(left).__name__ == type(right).__name__) and (left == right))
            return (bool(_eval_), "bool", id(_eval_))
        else:
            raise ValueError(f"Unsupported binary operator: {expr.operator}")

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)[0]
        right = self.evaluate(expr.right)[0]
        
        if expr.operator.lexeme == '&':
            _eval_ = bool(left and right)
            return (_eval_, "bool", id(_eval_))
        elif expr.operator.lexeme == '|':
            _eval_ = bool(left or right)
            return (_eval_, "bool", id(_eval_))
        else:
            raise ValueError(f"Unsupported logical operator: {expr.operator}")

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)[0]

        if expr.operator.lexeme == '!':
            _eval_ = bool(not right)
            return (_eval_, "bool", id(_eval_))
        elif expr.operator.lexeme == "-":
            _eval_ = float(-right)
            return (_eval_, "float", id(_eval_))
        elif expr.operator.lexeme == "+":
            _eval_ = float(+right)
            return (_eval_, "float", id(_eval_))
        elif expr.operator.lexeme == "++":
            _eval_ = float(right+1)
            return (_eval_, "float", id(_eval_))
        elif expr.operator.lexeme == "--":
            _eval_ = (right-1)
            return (_eval_, "float", id(_eval_))
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