

class Write:
    def __init__(self, args):
        self.args = args
        
    def write(self):
        for item in self.args:
            print(item, end=" ")
        print(end="\n")