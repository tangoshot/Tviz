'''
Created on Aug 8, 2012

@author: tkonik
'''



x = [1,1,1,2,2,2,3,3,3,1,1,1]


#def tanda(x):
#    for i in range(0, x.len):
#        for j= range(i, x.len):
#            if x[j+1] != x[j]:
#                yield i,j



def tanda(x, evalfn):
    i = j = 0
    while (i <len(x) and  j < len(x)):
        if j == len(x) - 1:
            yield i, j # Final exit condition
            return 
        
        if evalfn(x[j]) != evalfn(x[j + 1]):
            yield i , j
            i = j = j + 1
        else:
            j += 1

def identity(x):
    return x

for a,b in tanda(x, identity):
    print "---------"
    for s in range(a,b + 1):
        print s, ': ', x[s]
            
    
