from iassembly.lexer import *
from iassembly.interpreter import *

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
        def __init__(self, line, name, value):
            self.name = name
            self.index = value
            self.line = line
        
        def __repr__(self):
            return f"ListElementAccess=(name={self.name}, index={self.index}, line={self.line})"
        
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
            return self.handle_load_instruction()
        
        elif self.match(TokenType.CALL):
            return self.handle_function_call()
        
        elif self.match(TokenType.COMPUTE):
            return self.handle_compute_instruction()
        
        elif self.match(TokenType.LINK):
            return self.handle_Link_instruction()
        
        elif self.match(TokenType.CMP):
            return self.handle_compare_statement()
        
        elif self.match(TokenType.LABEL):
            return self.handle_label_template()
        
        elif self.match(TokenType.JUMP):
            return self.handle_jump_instruction()
        
        elif self.match(TokenType.DOT):
            return self.handle_loop_instruction()
        
        return self.expression()


    def handle_loop_instruction(self):
        line = self.peek().line
        self.consume(TokenType.LOOP, "Expected 'loop' keyword after dot (.), while creating as a loop")
        
        self.consume(TokenType.LEFT_BRACKET, "Expected '[' before loop for loop-statements enclosing, after loop OpCOde")
        initialize = self.expression()
        self.consume(TokenType.COMMA, "Expected ',' after loop-initializer example : .loop [eax, eax  <=  5, eax++] \n[....]")
        condition = self.expression()
        self.consume(TokenType.COMMA, "Expected ',' after loop-initializer example : .loop [eax, eax  <=  5, eax++] \n[....]")
        updating = self.expression()        
        self.consume(TokenType.RIGHT_BRACKET, "Expected ']' after loop for loop-statements enclosing, after loop OpCOde")
        
        self.consume(TokenType.LEFT_BRACKET, "Expected '[' after loop for loop-branches (statements-block) enclosing, after loop")
        loop_branch = self.consume_loop_block()
  
        return Expr.Loop(line, initialize, condition, updating, loop_branch)

    def consume_loop_block(self):
        block = []
        while not self.match(TokenType.RIGHT_BRACKET):
            block.append(self.declaration())
        return block
    

    def handle_jump_instruction(self):
        label_name = self.expression()
        return Expr.JumpInstruction(label_name)

    def handle_label_template(self):
        self.consume(TokenType.STAR, "Expected 'start' for starting  the label")
        self.consume(TokenType.COMMA, "Expected ',' after compute x [label x, y]")
        label_name = self.expression()
        label_block = self.consume_label_block()
        self.consume(TokenType.END, "Expected 'end' for ending the label")
        return Expr.LabelEntryFrame(label_name, label_block)
        
    def consume_label_block(self):
        block = []
        while not self.match(TokenType.LABEL):
            block.append(self.declaration())
        return block

    def handle_compare_statement(self):
        
        # Parse main condition (CMP)
        line_1 = self.peek().line
        self.consume(TokenType.LEFT_BRACKET, "Expected '[' before condition-statements enclosing, in cmp")
        cmp_condition = self.expression()
        self.consume(TokenType.RIGHT_BRACKET, "Expected ']' after condition-statements enclosing, in cmp")
        cmp_block = self.consume_condition_block()
        
        # Initialize for elif/else branches
        elif_branches = []
        
        # Handle ELIF branches (can be multiple)
        while self.match(TokenType.ELIF):
            line_2 = self.peek().line
            self.consume(TokenType.LEFT_BRACKET, "Expected '[' before condition-statements enclosing, in elif")
            elif_condition = self.expression()
            self.consume(TokenType.RIGHT_BRACKET, "Expected ']' after condition-statements enclosing, in elif")
            elif_block = self.consume_condition_block()
            elif_branches.append((elif_condition, elif_block))
        
        # Handle ELSE branch (optional)
        line_3 = self.peek().line
        if self.match(TokenType.ELSE):
            else_block = self.consume_condition_block()
        
        # Return the complete conditional structure
        return Expr.HandleCmpInstructions(
            cmp_condition,
            cmp_block,
            elif_branches,
            else_block,
            line_1,
            line_2,
            line_3
        )
        
    def consume_condition_block(self):
        block = []
        self.consume(TokenType.LEFT_BRACKET, "Expected '[' after before condition-code block enclosing")
        while not self.match(TokenType.RIGHT_BRACKET):
            block.append(self.declaration())
        return block

    def handle_Link_instruction(self):
        line = self.peek().line
        opponent_x = self.expression()
        self.consume(TokenType.COMMA, "Expected ',' after compute x [compute x, y]")
        opponent_y = self.expression()
        return Expr.LinkInstruction(opponent_x, opponent_y, line)

    def handle_compute_instruction(self):
        line = self.peek().line
        opponent_x = self.expression()
        self.consume(TokenType.COMMA, "Expected ',' after compute x [compute x, y]")
        self.consume(TokenType.LEFT_BRACKET, "Expected '[' after compute x [compute x, [y + z]]")
        opponent_y = self.expression()
        self.consume(TokenType.RIGHT_BRACKET, "Expected '[' after compute x [compute x, [y + z]]")
        return Expr.ComputeInstruction(opponent_x, opponent_y, line)


    def handle_function_call(self):
        line = self.peek().line
        opponent_x = self.expression()
        self.consume(TokenType.COMMA, "Expected ',' after call x [call x, y]")
        opponent_y = self.expression()
        return Expr.CallInstruction(opponent_x, opponent_y, line)

    def handle_load_instruction(self):
        line = self.peek().line
        opponent_x = self.expression()
        self.consume(TokenType.COMMA, "Expected ',' after load x [load x, y]")
        opponent_y = self.expression()
        return Expr.LoadInstruction(opponent_x, opponent_y, line)

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
            expr = Expr.Logical(self.peek().line, expr, operator, right)
        return expr

    def and_expr(self):
        expr = self.equality()
        while self.match(TokenType.CONDITIONAL_AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(self.peek().line, expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL, TokenType.DATA_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(self.peek().line, expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(self.peek().line, expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(self.peek().line, expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.MODULUS):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(self.peek().line, expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS, TokenType.PLUS, TokenType.INCREMENT, TokenType.DECREMENT):
            operator = self.previous()
            if operator.type in [TokenType.INCREMENT, TokenType.DECREMENT]:
                right = self.unary()  # Prefix increment/decrement (e.g., ++a, --a)
                return Expr.Unary(self.peek().line, operator, right)
            else:
                right = self.primary()  # Unary operations like `!` or `-`, `+`
                return Expr.Unary(self.peek().line, operator, right)
        return self.primary()

    def primary(self):
        
        if self.match(TokenType.FPTR):
            return Expr.CallPointerList("fptr")
        if self.match(TokenType.VPTR):
            return Expr.ValuePointerList("vptr")
        if self.match(TokenType.CPTR):
            return Expr.ComparePointerList("cptr")
        if self.match(TokenType.RPTR):
            return Expr.ReturnPointerList("rptr")
        
        if self.match(TokenType.EAX):
            return Expr.Register("eax")
        if self.match(TokenType.EBX):
            return Expr.Register("ebx")
        if self.match(TokenType.ECX):
            return Expr.Register("ecx")
        if self.match(TokenType.EDX):
            return Expr.Register("edx")
        if self.match(TokenType.EEX):
            return Expr.Register("eex")
        if self.match(TokenType.EFX):
            return Expr.Register("efx")
        if self.match(TokenType.EGX):
            return Expr.Register("egx")
        if self.match(TokenType.EHX):
            return Expr.Register("ehx")
        if self.match(TokenType.EIX):
            return Expr.Register("eix")
        if self.match(TokenType.EJX):
            return Expr.Register("ejx")
        if self.match(TokenType.EKX):
            return Expr.Register("ekx")
        if self.match(TokenType.ELX):
            return Expr.Register("elx")
        if self.match(TokenType.EMX):
            return Expr.Register("emx")
        if self.match(TokenType.ENX):
            return Expr.Register("enx")
        if self.match(TokenType.EOX):
            return Expr.Register("eox")
        if self.match(TokenType.EPX):
            return Expr.Register("epx")
        if self.match(TokenType.EQX):
            return Expr.Register("eqx")
        if self.match(TokenType.ERX):
            return Expr.Register("erx")
        if self.match(TokenType.ESX):
            return Expr.Register("esx")
        if self.match(TokenType.ETX):
            return Expr.Register("etx")
        if self.match(TokenType.EUX):
            return Expr.Register("eux")
        if self.match(TokenType.EVX):
            return Expr.Register("evx")
        if self.match(TokenType.EWX):
            return Expr.Register("ewx")
        if self.match(TokenType.EXX):
            return Expr.Register("exx")
        if self.match(TokenType.EYX):
            return Expr.Register("eyx")
        if self.match(TokenType.EZX):
            return Expr.Register("ezx")
        
        if self.match(TokenType.PAS):
            return Expr.PersistentRegister("pas")
        if self.match(TokenType.PBS):
            return Expr.PersistentRegister("pbs")
        if self.match(TokenType.PCS):
            return Expr.PersistentRegister("pcs")
        if self.match(TokenType.PDS):
            return Expr.PersistentRegister("pds")
        if self.match(TokenType.PES):
            return Expr.PersistentRegister("pes")
        if self.match(TokenType.PFS):
            return Expr.PersistentRegister("pfs")
        if self.match(TokenType.PXS):
            return Expr.PersistentRegister("pxs")
        if self.match(TokenType.PZS):
            return Expr.PersistentRegister("pzs")
        
        if self.match(TokenType.RAS):
            return Expr.ConstRegister("ras")
        if self.match(TokenType.RBS):
            return Expr.ConstRegister("rbs")
        if self.match(TokenType.RCS):
            return Expr.ConstRegister("rcs")
        if self.match(TokenType.RDS):
            return Expr.ConstRegister("rds")
        if self.match(TokenType.RES):
            return Expr.ConstRegister("res")
        if self.match(TokenType.RFS):
            return Expr.ConstRegister("rfs")
        if self.match(TokenType.RXS):
            return Expr.ConstRegister("rxs")
        if self.match(TokenType.RZS):
            return Expr.ConstRegister("rzs")
        
        if self.match(TokenType.INT):
            return Expr.INT(self.previous().literal)
        if self.match(TokenType.FLOAT):
            return Expr.FLOAT(self.previous().literal)
        if self.match(TokenType.FALSE):
            return Expr.BOOL(self.previous().lexeme)
        if self.match(TokenType.TRUE):
            return Expr.BOOL(self.previous().lexeme)
        if self.match(TokenType.NONE):
            return Expr.NONE(self.previous().lexeme)
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
        
        if self.match(TokenType.HANT_OPERATOR):
            line = self.peek().line
            name = self.expression()
            self.consume(TokenType.LEFT_BRACKET, "Expected '[' this, to enclose the index. while trying to access single list element")
            value = self.expression()
            self.consume(TokenType.RIGHT_BRACKET, "Expected ']' this, to enclose the index. while trying to access single list element")
            return Expr.AccessListItem(line, name, value)
        
        if self.match(TokenType.LEFT_BRACKET):
            line = self.peek().line
            elements = []
            while True:
                item = self.expression()
                elements.append(item)
                if not self.match(TokenType.COMMA):
                    break
            self.consume(TokenType.RIGHT_BRACKET, "Expected ']' closing list pair")
            return Expr.MakeHiddenList(elements, line)
            
        error_token = self.peek()
        self.error(error_token, "unexpected expression.", self.current)

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