

class Emit:
    def __init__(self, args):
        self.args = args
        
    def emit(self):
        buff = []
        for item in self.args:
            print(item)
            buff.append((len(item) if isinstance(item, str) else "true", type(item).__name__, id(item)))
    
        return buff