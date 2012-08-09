'''
Created on Aug 5, 2012
@author: tolga
'''
from tutil.string import normal_wordbag
from tviz.tvizdb import TvizSongFeatures


image_folder = 'C:/Media/Audio/Music/Released (k)/Tango (k)/Tango images (k)/'

orchestra_image_folder = image_folder + 'Orchestra images (k)'
singer_image_folder = image_folder + 'Singer images (k)'
label_image_folder = image_folder + 'Song images (k)'

IMPORTED_TAG_NAMES = [        
        'Name',
        'Orchestra',
        'Genre',
        'Singers']



        
class MySongFeatureFactory():
    
    tandagenres = frozenset(['vals', 'waltz', 'tango','milonga'])  

    @staticmethod
    def genre(tags):
        if not 'Genre' in tags:
            return None #TODO: HACK. this should happen at reading stage.
        
        tag = normal_wordbag(tags['Genre'])
        
        if 'walz' in tag:
            return 'vals'
        if 'tango' in tag:
            return 'tango'
        if 'milonga' in tag:
            return 'milonga'
        
        return None
    
    @staticmethod
    def singers(tags):
        return tags['Singers'].split(';')
    
    @staticmethod
    def orchestra(tags):
        print tags
        out = tags ['Orchestra']
        return out
        
    @staticmethod
    def name(tags):
        return tags ['Name']
    
   
    
        
    def infer(self, tags):
        obj = TvizSongFeatures()
        obj.name = self.name(tags)
        obj.genre = self.genre(tags)
        obj.isbreak = False if obj.genre else True
        obj.orchestra = self.orchestra(tags)
        obj.singers = self.singers(tags)
        
        nsingers = [x.lower() for x in obj.singers] # can we lower case UTF?
        if 'instrumental' in nsingers or 'i' in nsingers:
            obj.isinstrumental = True
        
        return obj
        
        
if __name__=='__main__':
    tags = {'Orchestra':'Canaro', 'Singers':'Fama;Podesta;Maida', 'Name':'Alma', 'Genre':'milonga candombe'}
    
    factory = MySongFeatureFactory()
    print factory.infer(tags)
    
    
