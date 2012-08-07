'''
Created on Jun 26, 2012

@author: tolga
'''

from web2py.gluon import template



if __name__ == '__main__':
    STR = '''
    <html>
    
    {{for x in [1,2,3]:}}
    {{print x}}
    {{pass}}
    </html>
    
    '''
    template.render(content=STR)
