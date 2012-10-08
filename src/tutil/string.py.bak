'''
Created on Jun 2, 2012

@author: Tolga Konik
'''



from unidecode import unidecode

import re

_word = re.compile('[a-zA-Z]+')

_first_cap_re = re.compile('(.)([A-Z][a-z]+)')

_all_cap_re = re.compile('([a-z0-9])([A-Z])')

def normal_wordbag(inputstr):        
        str1 = unidecode(inputstr)
        list1 = _word.findall(str1)
        str2 = ' '.join([uncamel(x) for x in list1]) # I could x + ' ' + uncamel and than push for partial results
        str3 = str2.replace('_', ' ')
        str4 = str3.lower()
        str4 = str4.encode('ascii')
        list2 = str4.split(' ')
        list2
        outputset = frozenset(list2)
        
        return outputset

def uncamel(name):
    s1 = _first_cap_re.sub(r'\1_\2', name)
    return _all_cap_re.sub(r'\1_\2', s1).lower()


if __name__ == '__main__':
    print normal_wordbag('xyABC d EFgh')