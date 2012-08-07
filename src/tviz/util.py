'''
Created on Jun 2, 2012

@author: Tolga Konik
'''

from unidecode import unidecode

def writef_error(string) :
    print "ERROR:" + string
    quit()    

def writef_warning(string) :
    print "WARNING:" + string    

def normal_wordbag(self, inputstr):        
        str1 = unidecode(inputstr)
        str2 = self.uncamel(str1)
        str3 = str2.lower()
        outputset = frozenset(self._word.findall(str3))
        return outputset
