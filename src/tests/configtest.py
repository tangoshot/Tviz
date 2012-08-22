'''
Created on Aug 17, 2012

@author: Tolga
'''



txt = open ('testsettings.py', 'r').read()

song = dict(GENRE='Tango')

exec(txt)

print GENRE
