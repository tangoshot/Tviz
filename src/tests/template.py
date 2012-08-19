'''
Created on Aug 8, 2012

@author: tkonik
'''
import gluon

from gluon import template

import logging
logging.basicConfig()


def f(x):
    return x * x

#print template.render( 
#content = 
#'''
#{{from test.template import f}} 
#
#<h1>
#{{for i in range(4,10):}}
# <h2> <{{=i}} : {{=f(i)}}> </h2>
#{{pass}}
#</h1>
#''', 
#context=dict(a=5))



# print template.render(content='<h>{{=u}}</h>',context=dict(u=u))
