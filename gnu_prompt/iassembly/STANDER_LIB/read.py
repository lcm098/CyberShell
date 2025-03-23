
class Read:
    
    def __init__(self, args):
        self.args = args
        
    def read_it(self):
        
        buff = []
        
        for item in self.args:
            if int(item) == 0: 
                user_input = input()
                buff.append((user_input, type(user_input).__name__, id(user_input)))
            
        return buff