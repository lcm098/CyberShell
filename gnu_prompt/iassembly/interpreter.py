from iassembly.parser import *
from iassembly.buffer import *
from iassembly.stdvar import StanderVariable
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
        self.pointer_environment = PointerStructure()
        self.stdvar = StanderVariable()
        self.addr_environment = AddressResolverStructure()
        self.StanderLib = StanderLibrary()
        
    
    def visit_Compute_instruction_call(self, inst):
        line = inst.line
        pointer_resolver = inst.pointer_resolver.lexeme
        expression = inst.expression.lexeme
        
        if pointer_resolver == self.stdvar.vptr:
            result = self.evaluate(expression)
            self.define_in_pointer_environment(pointer_resolver, result)
        else:
            raise InstructionError(f"{pointer_resolver} is a looking like 'vptr', which is very suitable. \n\tOn Line=[{line}]")
    
    
    def visit_System_function_call(self, inst):
        line = inst.line
        function_call_name = inst.function_call.lexeme
        pointer_linker = inst.pointer_linker.lexeme
        
        actual_args = []
        
        if self.pointer_environment.is_defined(pointer_linker) and pointer_linker == self.stdvar.fptr:
            actual_args = self.pointer_environment.get(pointer_linker)
            if self.is_list(actual_args):
                if self.StanderLib.check_right_system_function(function_call_name):
                    self.StanderLib.call_impropriated_function(function_call_name, actual_args)
                else:
                    # User Function Call Implemented here, leter
                    raise InstructionError(f"{function_call_name} is Not a stander Library Method. \n\tOn Line=[{line}]")
            else:
                raise InstructionError(f"Stander-Pointer resolver is not containing a list. \n\tOn Line=[{line}]")
        
        else:
            raise InstructionError(f"Stander-Pointer resolver fptr never used in this environment-block, before calling function. \n\tOn Line=[{line}]")
    
    def visit_Load_instruction(self, inst):
        line = inst.line
        stander_pointer = inst.stander_pointer.lexeme
        stander_variable = inst.stander_var.lexeme
        
        elements = []
        temp = []
        if self.is_special_pointer(stander_pointer):
                
            if self.is_stander_pointer(stander_variable):
                temp = self.addr_environment.get(stander_variable)
                
            elif (stander_variable == self.stdvar.rdo_var):
                temp = self.environment.get(stander_variable)
                
            else:
                raise InstructionError(f"Use Runtime-Read-Only Variable (rdo_var) or (Pointer-Resolver-Variable) at the place of '{stander_variable}'. \t\tOn Line=[{line}]")
                    
            if isinstance(temp, list):
                for item in temp:
                    elements.append(item[0])
                self.define_in_pointer_environment(stander_pointer, elements)
                
            else:
                raise InstructionError(f"Looking Like {temp[0]} is not an list, why?. \n\tOn Line=[{line}]")        
    
    
    def visit_Hidden_list_creation(self, inst):
        line = inst.line
        buffer = inst.elements_buff
        
        try:
            elements = []
            for item in range(len(buffer)):
                elements.append(self.evaluate(buffer[item]))
            
            self.define_in_rdo_var(elements, False)
            return elements
        
        except Exception as err:
            raise InstructionError(f"an error occurred \n\tOn Line=[{line}]")
        
    
    def visit_mov_instruction(self, inst):
        stander_variable = inst.stander_var.lexeme
        value = self.evaluate(inst.value)
        line = inst.line
        
        if self.is_stander_variable(stander_variable) and not self.is_list(value):
            self.define_in_environment(stander_variable, value, False)
            
        elif self.is_stander_pointer(stander_variable) and self.is_list(value):
            self.define_in_addr_environment(stander_variable, value, False)
        
        else:
            print(stander_variable)
            print(value)
            raise InstructionError(f"{stander_variable} is not a stander-instruction-variable. \n\tOn Line =[{line}]")
        
    
    def define_in_pointer_environment(self, stander_pointer, elements):
        if self.pointer_environment.is_defined(stander_pointer):
            self.pointer_environment.assign(stander_pointer, elements)
        else:
            self.pointer_environment.define(stander_pointer, elements, False)
        
        if self.environment.is_defined(self.stdvar.rdo_var):
            self.environment.assign(self.stdvar.rdo_var, elements)
        else:
            self.environment.define(self.stdvar.rdo_var, elements, False)    
        
    
    def is_special_pointer(self, stander_pointer):
        if (stander_pointer == self.stdvar.fptr) or (stander_pointer == self.stdvar.vptr) or (stander_pointer == self.stdvar.cptr):
            return True
        else:
            return False   
    
    def define_in_rdo_var(self, value, is_constant):
        
        if self.environment.is_defined(self.stdvar.rdo_var):
            self.environment.assign(self.stdvar.rdo_var, value)
        else:
            self.environment.define(self.stdvar.rdo_var, value, is_constant)
                
    def define_in_addr_environment(self, stander_variable, value, is_constant):
        if self.addr_environment.is_defined(stander_variable):
            self.addr_environment.assign(stander_variable, value)
        else:
            self.addr_environment.define(stander_variable, value, is_constant)
            
        if self.environment.is_defined(self.stdvar.rdo_var):
            self.environment.assign(self.stdvar.rdo_var, value)
        else:
            self.environment.define(self.stdvar.rdo_var, value, is_constant)
            
       
    def define_in_environment(self, stander_variable, value, is_constant):
        if self.environment.is_defined(stander_variable):
            self.environment.assign(stander_variable, value)
        else:
            self.environment.define(stander_variable, value, is_constant)
            
        if self.environment.is_defined(self.stdvar.rdo_var):
            self.environment.assign(self.stdvar.rdo_var, value)
        else:
            self.environment.define(self.stdvar.rdo_var, value, is_constant)
            
            
    def is_stander_pointer(self, stander_variable):
        if (stander_variable == self.stdvar.ecx_res) or (stander_variable == self.stdvar.edx_res) or (stander_variable == self.stdvar.eex_res) or (stander_variable == self.stdvar.efx_res) or (stander_variable == self.stdvar.egx_res) or (stander_variable == self.stdvar.ehx_res) or (stander_variable == self.stdvar.eix_res):
            return True
        else:
            return False
        
    def is_stander_variable(self, stander_variable):
        if (stander_variable == self.stdvar.ras) or (stander_variable == self.stdvar.rbs) or (stander_variable == self.stdvar.rcs) or (stander_variable == self.stdvar.rds) or (stander_variable == self.stdvar.res) or (stander_variable == self.stdvar.rfs) or (stander_variable == self.stdvar.rgs):
            return True
        else:
            return False
        
    def is_list(self, item):
        if isinstance(item, list):
            return True
        else:
            return False
        
        
    def visit_identifier(self, inst):
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