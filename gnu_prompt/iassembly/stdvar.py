

class StdVar:
    
    class Normal:
        def __init__(self):
            self.eTypeRegister = "register"
        
        def isNormal(self, register):
            CheckNormalType = (self.eTypeRegister,)
            if register in CheckNormalType:
                return True
            else:
                return False
            
    
    class Stander:
        
        def __init__(self):
            
            self.vTypeRegister = "vptr"
            self.fTypeRegister = "fptr"
            self.cTypeRegister = "cptr"
            self.rTypeRegister = "rptr"
        
        def isStander(self, register):
            CheckStanderType = (self.vTypeRegister, self.fTypeRegister, self.cTypeRegister, self.rTypeRegister)
            if register in CheckStanderType:
                return True
            else:
                return False
        
    class Object:
        
        def __init__(self):
        
            self.iType = "identifier"
            self.pType = "persistent"
            self.cType = "const"
        
        def isObject(self, register):
            CheckObjectType = (self.iType, self.pType, self.cType)
            if register in CheckObjectType:
                return True
            else:
                return False
            
            