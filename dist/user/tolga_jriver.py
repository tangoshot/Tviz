'''
Created on Aug 17, 2012
@author: tolga
'''

#######################
# GENRE
#######################

genrewords = tagwords('Genre', 'Subgroup')

GENRE = ''

if 'vals' in genrewords or 'walz' in genrewords:
    GENRE = 'Vals'
    
if 'milonga' in genrewords:
    GENRE = 'Milonga'

if 'tango' in genrewords:
    GENRE = 'Tango'
 
if 'alternative' in genrewords  or  'nontraditional' in genrewords:
    GENRE = 'Alternative' + GENRE
    
#######################
# SINGERS
#######################
instrumentaltags = ['instrumental', 'Instrumental', 'isinstrumental']

SINGERS = tag('Singer').split(';')
SINGERS = [singer for singer in SINGERS if not singer in instrumentaltags]
    # remove instrumental markers from SINGERS LIST
    
#######################
# ORCHESTRA
#######################

ORCHESTRA = tag('Orchestra')

#######################
# NAME
#######################

NAME = tag('Name')

#######################
# ISBREAK
#######################
    
if GENRE:
    ISBREAK = False
else:
    ISBREAK = True

#######################
# ISINSTRUMENTAL
#######################

ISINSTRUMENTAL = False

if 'instrumental' in tagwords('Singer') or 'isinstrumental' in tagwords('Singer'):
    ISINSTRUMENTAL = True

