from iassembly.environment import environment

class Read:
    
    def __init__(self, args):
        self.args = args
        self.environment = environment
        
    def read(self):
        
        buff = []
        
        for item in  self.args:
             
            temp = str(input(""))
            if self.environment.is_defined(item, item, id(item)):
                self.environment.assign((item, item, id(item)), (temp, type(item).__name__, id(item)))
            else:
                self.environment.define((item, item, id(item)), (temp, type(item).__name__, id(item)), False)
            buff.append((item, type(item).__name__, id(item)))
            
        return buff