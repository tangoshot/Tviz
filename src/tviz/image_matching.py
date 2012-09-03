'''
Created on Aug 5, 2012

@author: tolga
'''
import os
from settings import label_image_folder, orchestra_image_folder, singer_image_folder
from tutil.string import normal_wordbag

class ImageDb():

    _imagefolders = [
        orchestra_image_folder, 
        singer_image_folder]
        # , label_image_folder]
    
    _imageexts = frozenset(['gif', 'jpg', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'webp'])
    _db = {}
    
    def __init__(self, options):
        self.reset(options)
    
    def __str__(self):
        
            return '\n'.join([str(key) + ' : ' + str(self._db[key]) for key in self._db])

    def reset(self, options):
        
        #for imagefolder in self._imagefolders:
        for directory, _subdirs, files in os.walk(options.IMAGE_FOLDER):
            for f in files:
                imagefile = os.path.join(directory,f) 
                
                base = os.path.basename(f)
                
                rawwordbag = normal_wordbag(base)
                
                if rawwordbag & self._imageexts != []:
                    wordbag = rawwordbag - self._imageexts
                    # print wordbag,  imagefile
                    self._db [wordbag] = imagefile 
                    # for each word bag, only one image file is stored.
            
    # TODO: implement best match
    def find(self, input):
        # print self
        # print "Find: ", input
        
        input = normal_wordbag(input)
        # print "query: ", input
        
        if input in self._db:
            try:
                outstr = self._db[input]
            except:
                print "Cannot find %s in image database\n" % input
            
            return outstr
        
        # TODO: partial find
        return None
        



if __name__ == '__main__':
    
    imagefinder = ImageDb()
#    print imagefinder._normalize_wordbag("DiSarli")
#    print imagefinder._normalize_wordbag("diSarli")
#    print imagefinder._normalize_wordbag("dArienzo")
#    print imagefinder._normalize_wordbag("d'Arienzo")
#    print imagefinder._normalize_wordbag("D'arienzo")
    
    imagefinder.reset()
    
    
    d = imagefinder._db
    
    for x in d:
        print x, ":", d[x]

    for s in ['Canaro', 'Di Sarli', "D'Arienzo", "Podesta, Alberto "]:
        print s, ':', imagefinder.find(s)
        
        print imagefinder.find('rojas alfredo')
        
