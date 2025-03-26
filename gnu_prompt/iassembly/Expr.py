class Expr:
        
    class Binary:
        def __init__(self, line, left, operator, right):
            self.line = line
            self.left = left
            self.operator = operator
            self.right = right
        
        def __repr__(self):
            return f"Binary(left={self.left}, operator={self.operator}, right={self.right})"

        def accept(self, visitor):
            return visitor.visit_binary_expr(self)
        
    class Logical:
        def __init__(self, line, left, operator, right):
            self.line = line
            self.left = left      # Left-hand side expression
            self.operator = operator  # Operator (AND/OR)
            self.right = right    # Right-hand side expression

        def accept(self, visitor):
            return visitor.visit_logical_expr(self)
        
    class Unary:
        def __init__(self, line, operator, right):
            self.line = line
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

    class NONE:
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"Literal(value={None})"
        
        def accept(self, visitor):
            return visitor.visit_none_expr(self)
        
    
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
        
    class CallPointerList:
        def __init__(self, pointer):
            self.pointer = pointer
        
        def __repr__(self):
            return f"fptr=({self.pointer})"
        
        def accept(self, visitor):
            return visitor.visit_call_pointer_list(self)
    
    class ValuePointerList:
        def __init__(self, pointer):
            self.pointer = pointer
        
        def __repr__(self):
            return f"vptr=({self.pointer})"
        
        def accept(self, visitor):
            return visitor.visit_value_pointer_list(self)
    
    class ComparePointerList:
        def __init__(self, pointer):
            self.pointer = pointer
        
        def __repr__(self):
            return f"cptr=({self.pointer})"
        
        def accept(self, visitor):
            return visitor.visit_compare_pointer_list(self)
    
    class MakeHiddenList:
        def __init__(self, elements, line):
            self.elements = elements
            self.line = line
        
        def __repr__(self):
            return f"HiddenList=({self.elements}, {self.line})"
        
        def accept(self, visitor):
            return visitor.visit_make_hidden_list(self)
    
    class LoadInstruction:
        def __init__(self, opponent_x, opponent_y, line):
            self.opponent_x = opponent_x
            self.opponent_y = opponent_y
            self.line = line
        
        def __repr__(self):
            return f"load instruction=({self.opponent_x}, {self.opponent_x}, {self.line})"
        
        def accept(self, visitor):
            return visitor.visit_load_instruction(self)
    
    class CallInstruction:
        def __init__(self, opponent_x, opponent_y, line):
            self.opponent_x = opponent_x
            self.opponent_y = opponent_y
            self.line = line
        
        def __repr__(self):
            return f"call instruction=({self.opponent_x}, {self.opponent_x}, {self.line})"
        
        def accept(self, visitor):
            return visitor.visit_call_instruction(self)
    
    class ComputeInstruction:
        def __init__(self, opponent_x, opponent_y, line):
            self.opponent_x = opponent_x
            self.opponent_y = opponent_y
            self.line = line
        
        def __repr__(self):
            return f"compute instruction=({self.opponent_x}, {self.opponent_x}, {self.line})"
        
        def accept(self, visitor):
            return visitor.visit_compute_instruction(self)
    
    class LinkInstruction:
        def __init__(self, opponent_x, opponent_y, line):
            self.opponent_x = opponent_x
            self.opponent_y = opponent_y
            self.line = line
        
        def __repr__(self):
            return f"link instruction=({self.opponent_x}, {self.opponent_x}, {self.line})"
        
        def accept(self, visitor):
            return visitor.visit_link_instruction(self)
    
    
    class PersistentRegister:
        def __init__(self, persis):
            self.persis = persis
        
        def __repr__(self):
            return f"persis=({self.persis})"
        
        def accept(self, visitor):
            return visitor.visit_persistent_register(self)
        
        
    class ConstRegister:
        def __init__(self, const):
            self.const = const
        
        def __repr__(self):
            return f"const=({self.const})"
        
        def accept(self, visitor):
            return visitor.visit_const_register(self)
        
        
    class ReturnPointerList:
        def __init__(self, pointer):
            self.pointer = pointer
        
        def __repr__(self):
            return f"rptr=({self.pointer})"
        
        def accept(self, visitor):
            return visitor.visit_rptr_pointer(self)
    
    
    class AccessListItem:
        def __init__(self, line, name, indices):
            self.name = name
            self.indices = indices
            self.line = line
        
        def __repr__(self):
            return f"ListElementAccess=(name={self.name}, index={self.indices}, line={self.line})"
        
        def accept(self, visitor):
            return visitor.visit_list_element_access(self)
    
    
    class HandleCmpInstructions:
        def __init__(self, cmp_condition, cmp_branches, elif_branches, else_block, line_1, line_2, line_3):
            self.cmp_condition = cmp_condition
            self.cmp_branches = cmp_branches
            self.elif_branches = elif_branches
            self.else_block = else_block
            self.line_1 = line_1
            self.line_2 = line_2
            self.line_3 =  line_3
            
        def __repr__(self):
            return f"""HandleCmpInstructions=(line={self.line_1} cmp_condition={self.cmp_condition}
                    cmp_branches={self.cmp_branches}, line={self.line_2})
                    elif_branches={self.elif_branches}, line={self.line_3} else_block={self.else_block}"""
        
        def accept(self, visitor):
            return visitor.visit_cmp_handler(self)
        
    
    class LabelEntryFrame:
        def __init__(self, label_name, label_block):
            self.label_name = label_name
            self.label_block = label_block
        
        def __repr__(self):
            return f"LabelEntryFrame=(label_name=({self.label_name}), label_block=({self.label_block}))"
        
        def accept(self, visitor):
            return visitor.visit_label_entry_frame(self)
    
    class JumpInstruction:
        def __init__(self, label_name):
            self.label_name = label_name
        
        def __repr__(self):
            return f"JumpInstruction=(label_name=({self.label_name}))"
        
        def accept(self, visitor):
            return visitor.visit_jump_instruction(self)
        
    class Loop:
        def __init__(self, line, initialize, condition, updating, loop_branch):
            self.line = line
            self.initialize = initialize
            self.condition = condition
            self.updating = updating
            self.loop_branch = loop_branch
            
        def __repr__(self):
            return f"LoopInstruction(line={self.line}, condition={self.condition}, updating={self.updating}, loop-branch={self.loop_branch})"
        
        def accept(self, visitor):
            return visitor.visit_loop_instruction(self)
        
    class MakeHiddenDict:
        
        def __init__(self, _dict_, line):
            self._dict_ = _dict_
            self.line = line
        
        def __repr__(self):
            return f"HiddenList=({self._dict_}, {self.line})"
        
        def accept(self, visitor):
            return visitor.visit_make_hidden_dict(self)