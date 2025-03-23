from iassembly.STANDER_LIB.write import *
from iassembly.STANDER_LIB.read import *
from iassembly.STANDER_LIB.emit import *

class StanderLibrary:
    
    def __init__(self):
        self.buff = ["write", "read", "emit"]  

    def check_right_system_function(self, func_name):
        return func_name in self.buff

    def call_impropriated_function(self, func_name, args):
        
        match func_name:
            case "write":
                return self.call_write(args)

            case "read":
                return self.call_read(args)
            
            case "emit":
                return self.call_emit(args)
                
            case _:
                return False
            

    def call_write(self, args):
        
        _write_ = Write(args)
        return _write_.write()
        
    def call_read(self, args):
        _read_ = Read(args)
        return _read_.read_it()
    
    def call_emit(self, args):
        _emit_ = Emit(args)
        return _emit_.emit()