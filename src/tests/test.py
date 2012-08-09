'''
Created on Jun 26, 2012

@author: tolga
'''

from gluon import template
from gluon import P

def f(x):
    return P(x * x)


if __name__ == '__main__':
    STR = '''
<html>
{{for x in [1,2,3]:}}
<h1> {{=x}} {{=f(x)}} </h1>
{{pass}}
</html>

'''
    print template.render(content=STR, context = dict(x='z', f=f))
