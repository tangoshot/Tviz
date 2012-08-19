'''
Created on Aug 8, 2012

@author: tkonik
'''



def tandait(lst, evalfn):
    i = 0
    j = 1

    while (i <len(lst) and  j <= len(lst)):

        if j == len(lst) or evalfn(lst[j]) != evalfn(lst[j - 1]):
            yield i , j, lst[i : j]
            i = j 
        
        j += 1

    
if __name__ == '__main__':
    lst = [1,1,1,2,2,2,3,3,3,1,1,1,5]
    
    def identity(x):
        return x
    
    for (a,b,c) in tandait(lst, identity):
        print a,b,c
