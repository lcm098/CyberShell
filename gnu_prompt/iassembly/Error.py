class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
    def __repr__(self):
        return self.message
    
    
class LexerError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __repr__(self):
        return self.message
    
    
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
    
    
class Throw_Error(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __repr__(self):
        return self.message