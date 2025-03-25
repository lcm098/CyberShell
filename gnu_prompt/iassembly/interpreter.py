from iassembly.parser import *
from iassembly.buffer import *
from iassembly.stdlib import *
from iassembly.buffer import *
from iassembly.stdvar import StdVar

class ExprVisitor:
        
    """
    Abstract visitor class for visiting expressions in the abstract syntax tree.
    Each visit method corresponds to a specific type of expression.
    """

    def accept(self, visitor):
        raise NotImplementedError("Subclasses must implement accept method")

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
        self.persistent_values = {}  # Store for persistent registers
        self.Object = StdVar.Object()
        self.Stander = StdVar.Stander()
        self.Normal = StdVar.Normal()
        
        
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
    
    
    def visit_loop_instruction(self, inst):
        line = inst.line
        initialize = self.evaluate(inst.initialize)
        condition = inst.condition
        updating = inst.updating
        loop_branch = inst.loop_branch
        
        if self.Normal.isNormal(initialize[1]):
            while True:
                condition_result = self.evaluate(condition)[0]
                if not condition_result:
                    break
                
                self.execute_block(loop_branch)
                update_value = self.evaluate(updating)
                self.push_in_environment(initialize, update_value)
                
        else:
            raise InstructionError(f"initializer or updating register is not eTypeRegister like (eax, ebx...) category")
        
    
    def visit_label_entry_frame(self, inst):
        label_name = self.evaluate(inst.label_name)[0]
        label_block = inst.label_block
        
        if self.environment.is_defined(label_name):
            raise InstructionError(f"Fuck, The Label with name {label_name} already  defined at two places")
        else:
            # 1. it will define for later jump call to execute this label
            # 2. execute label function written for current execution of label,
            # i mean, i want to say, it do not have to behave like function
            self.environment.define(label_name, label_block)
            self.execute_block(label_block)
        
        
    def visit_jump_instruction(self, inst):
        label_name = self.evaluate(inst.label_name)[0]
        
        if self.environment.is_defined(label_name):
            label_block = self.environment.get(label_name)
            self.execute_block(label_block)
        else:
            raise InstructionError(f"Fuck again, The Label with name {label_name} is not defined in current environment scope. why?")
    
    
    def visit_cmp_handler(self, inst):
        
        cmp_condition = inst.cmp_condition
        cmp_branches = inst.cmp_branches
        elif_branches = inst.elif_branches
        else_block = inst.else_block
        line1 = inst.line_1
        line2 = inst.line_2
        line3 = inst.line_3

        if self.evaluate(cmp_condition)[0]:
            self.execute_block(cmp_branches)
            return

        for elif_condition, elif_block in elif_branches:
            if self.evaluate(elif_condition)[0]:
                self.execute_block(elif_block)
                return

        if else_block:
            self.execute_block(else_block)
            
    
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
            y_value = self.is_opponent_y_regis(name, line)
            
            if isinstance(y_value, list):
                
                list_size = len(y_value)
                if index[0] <= list_size:
                    final_list_element = y_value[index[0]]
                    return final_list_element
                else:
                    raise InstructionError(f"List Element Access : [access's size exceeded], size must be <= {list_size}, \n\tOn Line=[{line}]")
            else:
                raise InstructionError(f"What The Fuck : [you are trying to access '{y_value}'s' element, which is not a list]")
        else:
            raise InstructionError(f"List {name} is not defined. \n\tOn Line=[{line}]")
    
    
    def visit_load_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if self.Normal.isNormal(opponent_x[1]) and self.Stander.isStander(opponent_y[1]):
            y_value = self.is_opponent_y_regis(opponent_y, line)
            self.push_in_environment(opponent_x, y_value)
            
        else:
            raise InstructionError(f"invalid load x, y combination, where x should be (eTypeRegister) and y should be(v,c,f,r)TypeRegister only. \n\tOn Line =[{line}]")
        pass
        
    def visit_call_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if opponent_y[1] == self.Stander.fTypeRegister:
            while not isinstance(opponent_y, list):
                opponent_y = self.is_opponent_y_regis(opponent_y, line)
            
            clean_list = []
            for item in opponent_y:
                clean_list.append(item[0])
            
            if opponent_x[1] == self.Object.iType and isinstance(opponent_y, list):
                if self.StanderLib.check_right_system_function(opponent_x[0]):
                    
                    return_value = self.StanderLib.call_impropriated_function(opponent_x[0], clean_list)
                    self.push_in_environment((self.Stander.rTypeRegister, self.Stander.rTypeRegister, id(self.Stander.rTypeRegister)), return_value)
                    
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
        
        if opponent_x[1] == self.Stander.vTypeRegister:
            y_value = self.is_opponent_y_regis(opponent_y, line)
            self.push_in_environment(opponent_x, y_value)
        else:
            raise InstructionError(f"Unable to store value in {opponent_x}, use opponent 'v(Register)Type'. \n\tOn Line=[{line}]")
    
    def visit_link_instruction(self, inst):
        line = inst.line
        opponent_x = self.evaluate(inst.opponent_x)
        opponent_y = self.evaluate(inst.opponent_y)
        
        if self.Stander.isStander(opponent_x[1]):
            if opponent_y[1] in (self.Normal.eTypeRegister):
                y_value = self.is_opponent_y_regis(opponent_y, line)
                self.push_in_environment(opponent_x, y_value)
            else:
                raise InstructionError(f"Unable to store value {opponent_y} in {opponent_x}, use opponent 'v(Register)Type'. \n\tOn Line=[{line}]")
        else:
            raise InstructionError(f"opponent_y expected as (e)Type or (v)Type register but, i got {opponent_y}")
            
    def visit_mov_instruction(self, inst):
        try:
            line = inst.line
            opponent_x = self.evaluate(inst.opponent_x)
            opponent_y = self.evaluate(inst.opponent_y)
            
            # Handle const registers - prevent modification after initialization
            if opponent_x[1] == self.Object.cType:
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
            if opponent_x[1] == self.Object.pType:
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
            if opponent_x[1] == self.Normal.eTypeRegister:
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
            if self.Normal.isNormal(item[1]) or self.Stander.isStander(item[1]) or self.Object.isObject(item[1]):
                value = self.environment.get(item)
                if isinstance(value, list):
                    clean.append(self.make_clean_list(value))
                else:
                    clean.append(value)
            else:
                clean.append(item)
        return clean
        
    def is_opponent_y_regis(self, y, line):
        if (isinstance(y, list) or isinstance(y, tuple)) and self.Normal.isNormal(y[1]) or self.Stander.isStander(y[1]) or self.Object.isObject(y[1]):
            if self.environment.is_defined(y):
                value = self.environment.get(y)
                # Check if the value is a list or another register reference
                if isinstance(value, list):
                    return value  # Return the list directly
                elif self.Normal.isNormal(y[1]) or self.Stander.isStander(y[1]) or self.Object.isObject(y[1]):
                    return self.is_opponent_y_regis(value, line)
                else:
                    return value
            else:
                # Special handling for persistent registers that might exist in persistent store
                if y[1] == self.Object.pType and y[0] in self.persistent_values:
                    return self.persistent_values[y[0]]
                raise InstructionError(f"using of {y} without initialing it, before.")
        else:
            return y
            
    def push_in_environment(self, x, y, is_const=False):
        if x[1] == self.Object.cType:
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
            value = self.is_opponent_y_regis(identifier)
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
        
        # Get the left and right operands
        left_value = self.evaluate(expr.left)
        right_value = self.evaluate(expr.right)
        
        # Resolve identifiers and registers to their actual values
        left = self.is_opponent_y_regis(left_value, expr.line)[0]
        right = self.is_opponent_y_regis(right_value, expr.line)[0]

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
        
        elif expr.operator.lexeme == '<=':
            _eval_ = left <= right
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
        
        # Get the left and right operands
        left_value = self.evaluate(expr.left)
        right_value = self.evaluate(expr.right)
        
        # Resolve identifiers and registers to their actual values
        left = self.is_opponent_y_regis(left_value, expr.line)[0]
        right = self.is_opponent_y_regis(right_value, expr.line)[0]
        
        if expr.operator.lexeme == '&':
            _eval_ = bool(left and right)
            return (_eval_, "bool", id(_eval_))
        elif expr.operator.lexeme == '|':
            _eval_ = bool(left or right)
            return (_eval_, "bool", id(_eval_))
        else:
            raise ValueError(f"Unsupported logical operator: {expr.operator}")

    def visit_unary_expr(self, expr):
        
        right_value = self.evaluate(expr.right)
        right = self.is_opponent_y_regis(right_value, expr.line)[0]

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
    