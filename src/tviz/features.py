'''
Created on Aug 5, 2012

@author: tolga
'''

class SongFeatures(object):
    '''
    inferred features of a song
    '''
    self.name = None
    self.orchestra = None
    self.singerlist = []
    self.genre = None
    self.isbreak = None
    
    self.tandagenres = frozenset(['vals', 'waltz', 'tango','milonga'])  

class TandaFeatures(object):
    '''
    inferred features of a tanda
    '''

        
class MySongFeatures(SongFeatures):
    _tags = None
    
    def __init__(tags):
        self._tags = tags
        self.name = self.name()
        self.genre = self.genre()
        self.isbreak = False if self.genre else True
        self.orchestra = self.orchestra()
        self.singers = self.singers()
        

    def genre(self):
        tag = normal_wordbag(tags['Genre'])
        
        if 'walz' in tag:
            return 'vals'
        if 'tango' in tag:
            return 'tango'
        if 'milonga' in tag:
            return 'milonga'
        
        return None
    
    def singers(self):
        return tags['Singers'].split(';')
            
    def orchestra(self):
        return tags ['Orchestra']
        
    def name(self):
        return tags ['Name']
        
class MyTandaFeatures(TandaFeatures):
    pass

