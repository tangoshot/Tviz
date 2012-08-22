import types

class ClassPPrinter:

    def __str__(self):
        
        out= ''
        for attr in dir(self):
            value = getattr(self, attr)
            if not attr [0] == '_' and not isinstance(value, types.MethodType):
                out = out + attr + ' : ' + str(value) + '\n'
        return out



class ClassAttribProtector:
    
    def __setattr__ (self, name, value):
        # print "Name:", name
        # print "value: ", value
        
        if name not in dir(self): 
            raise Exception('Unknown Static Feature: ' + name)
        
        self.__dict__ [name] = value