'''
Created on Jun 30, 2012

@author: tolga
'''

import urllib

url = 'http://developer.yahoo.com/'
u = urllib.urlopen(url)
# u is a file-like object
data = u.read()
