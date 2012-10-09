'''
Created on Aug 5, 2012
@author: tolga
'''
from tutil.string import normal_wordbag

import re
from tutil.meta import ClassPPrinter, ClassAttribProtector
from paths import options_file, mapping_file
import logging

TAG_FUNCTIONS = ['tag', 'tagwords']


'''
Created on Aug 11, 2012


@author: tolga
'''

class Features (ClassPPrinter):
    index2features = {
        'name', 
        'genre',
        'isbreak',
        'orchestra',
        'singers',
        'key',
        'filename',
        'isinstrumental'}
    
    
    def __init__(self, fdict = {}):
        for feature in self.index2features:
            setattr(self, feature, fdict[feature])
   
 
    


class TvizSong(ClassPPrinter):
    name = None
    orchestra = None
    singerlist = []
    genre = None
    isbreak = None
    isinstrumental = None
    key = None
    
    def __str__ (self):
            wordlist = [   
                "name:           ", str(self.name), "\n", 
                "orchestra:      ", str(self.orchestra), "\n",
                "genre:          ", str(self.genre), "\n",
                "isbreak:        ", str(self.isbreak), "\n",
                "isinstrumental: ", str(self.isinstrumental), "\n",
                "singers:        ", str(self.singers), '\n' 
                "key:        ",     str(self.key), '\n']
            
            return ''.join(wordlist)
    
class TvizSongFeatures(TvizSong):
    ## MISSING Instrumental marker
    
    '''
    inferred index2features of a song
    '''


    
class TvizTandaFeatures(TvizSongFeatures):
    orchestra = None
    singerlist = None
    GENRE = None
    isbreak = None

    def __str__ (self):
        
        wordlist = [   
            "orchestra: %s" % unidecode(str(self.orchestra)),
            "GENRE: %s" % unidecode(str(self.genre)),
            "isbreak: %s" % unidecode(str(self.isbreak)),
            "singers:  %s" % unidecode(str(list(self.singers)))]
        
        return '\n'.join(wordlist)

class UserOptions (ClassPPrinter):
    # TODO: add type checking to static index2features

    index2features = dict(
        USER = str,
        PWD = str,
        PORT = int,
        PLAYER = str,
        IMAGE_FOLDER = str,
        PROFILE = str )

    def __init__(self, optionsname):
        sfile= options_file(optionsname)
        
        localdict = {}
        execfile(sfile , globals(), localdict)
        
        for feature in self.index2features:
            try:
                setattr(self, feature, localdict[feature])
            except Exception as e:
                
                logging.error('Missing feature "{feature}" in user file: {file}'.format(
                        feature = feature,
                        file = sfile))
                
                raise e
            
            
        
        self.update(localdict)


    def update(self, dictionary):
        self.USER =        dictionary['USER']
        self.PWD =         dictionary['PWD']
        self.PORT =        dictionary['PORT']
        self.PLAYER =      dictionary['PLAYER']                
        self.IMAGE_FOLDER = dictionary['IMAGE_FOLDER']

    
class UserFeatureFactory (ClassPPrinter):

    # TODO: add type checking and coverage checking to dynamic index2features
    tagnames = []

    index2features = {
        'NAME', 
        'GENRE',
        'ISBREAK',
        'ORCHESTRA',
        'SINGERS',
        'ISINSTRUMENTAL'}
    
    
    def __init__(self, settings):
        self.__user_mapping_file = mapping_file(settings)
        usermapping = open(self.__user_mapping_file, 'r').read()
        self.tagnames = self.__parse_tags(usermapping)
        
    def tags2features(self, tags):
        ''' 
        Infers feature values give user definitions and a set of song tags
        '''
        
        def tag(tagname):
            return tags[tagname]
        
        def tagwords(*tagnames):
            out = set()
            for tagname in tagnames:
                out = out or normal_wordbag(tags[tagname])
                return out
        
        localdict = dict(tag = tag, tagwords = tagwords)

        sfile = self.__user_mapping_file
        execfile(sfile, globals(), localdict)

        out = {}

        for feature in self.index2features:
            try:
                out[feature.lower()] = localdict[feature]
            except Exception as e:
                logging.error('Missing feature "{feature}" in user tagging file: {file}'.format(
                    feature = feature,
                    file = sfile))
                raise e
                
        return out
   
    def __parse_tags (self, txt):
        argpat = '\(([^\)]*)\)' 

        stringpat1 = '"([^"]*)"'
        stringpat2 = "'([^']*)'"
        
        out = []
        
        for f in TAG_FUNCTIONS:
            funcpattern = f + argpat
            argstrlist = re.findall(funcpattern, txt)

            for argstr in argstrlist:
                out = out + re.findall(stringpat2, argstr)
                out = out + re.findall(stringpat1, argstr)
            
        out = list(set(out))
        
        return out
        
if __name__=='__main__':
    tags = {'Orchestra':'Canaro', 'Singer':'Fama;Podesta;Maida', 'Name':'Alma', 'Genre':'milonga candombe', 'Key':'124252', 'Subgroup':'Traditional'}
    
    print '-------------------------------'
    print 'Static User Features'
    print '-------------------------------'

    o = UserOptions('config')
    print o

    print '-------------------------------'
    print 'Dynamic User Features'
    print '-------------------------------'
    
    f = UserFeatureFactory('tagging')
    f.tags2features(tags)
    print f
    

