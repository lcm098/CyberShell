from iassembly.STANDER_LIB.write import *

class StanderLibrary:
    
    def __init__(self):
        self.buff = ["write"]  

    def check_right_system_function(self, func_name):
        return func_name in self.buff

    def call_impropriated_function(self, func_name, args):
        
        match func_name:
            case "write":
                self.call_write(args)

            case _:
                return False
            

    def call_write(self, args):
        
        _write_ = Write(args)
        _write_.write()
        