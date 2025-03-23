

class Write:
    def __init__(self, args):
        self.args = args
        
    def write(self):
        buff = []
        for item in self.args:
            print(item, end=" ")
            buff.append((len(item) if isinstance(item, str) else "true", type(item).__name__, id(item)))
        
        print(end="\n")
        return buff