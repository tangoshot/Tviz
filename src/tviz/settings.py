'''
Created on Aug 5, 2012
@author: tolga
'''
from tutil.string import normal_wordbag
from tviz.feature_factory import TvizSongFeatures
# from tviz.tvizdb import TvizSongFeatures
from paths import SETTINGS

USER = 'mc'
PWD = 'mc'
PORT = '50001'

image_folder = 'C:/Media/Audio/Music/Released (k)/Tango (k)/Tango images (k)/'

orchestra_image_folder = image_folder + 'Orchestra images (k)'
singer_image_folder = image_folder + 'Singer images (k)'
label_image_folder = image_folder + 'Song images (k)'


        
class MySongFeatureFactory():
    
    def tags2features(self, tags):
        obj = TvizSongFeatures()
        
        def tag(tagname):
            return tags[tagname]
        
        def tagwords(*tagnames):
            out = set()
            for tagname in tagnames:
                out = out or normal_wordbag(tags[tagname])
                return out
        
        locals = dict(tag = tag, tagwords = tagwords)
            
        execfile(SETTINGS + '/user.py', globals(),locals)
        
        
        obj.name = locals['name']
        obj.genre = locals['genre']
        obj.isbreak = locals['isbreak']
        obj.orchestra = locals['orchestra']
        obj.singers = locals['singers']
        obj.key = locals['key']
        obj.isinstrumental = locals['isinstrumental']

        return obj
        
        
if __name__=='__main__':
    tags = {'Orchestra':'Canaro', 'Singer':'Fama;Podesta;Maida', 'Name':'Alma', 'Genre':'milonga candombe', 'Key':'124252', 'Subgroup':'Traditional'}
    
    factory = MySongFeatureFactory()
    print factory.tags2features(tags)
    
    
