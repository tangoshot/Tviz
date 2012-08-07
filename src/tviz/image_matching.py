'''
Created on Aug 5, 2012

@author: tolga
'''
import os
import re
from settings import label_image_folder, orchestra_image_folder, singer_image_folder
from os.path import join
from tviz.util import normal_wordbag

class ImageDb():

    _imageexts = frozenset(['gif', 'jpg', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'webp'])
    _db = {}
    _first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    _all_cap_re = re.compile('([a-z0-9])([A-Z])')
    _word = re.compile('[a-z]+')

    def reset(self):
        for imagefolder in [label_image_folder, orchestra_image_folder, singer_image_folder]:
            for dir, _subdirs, files in os.walk(imagefolder):
                for f in files:
                    imagefile = os.path.join(dir,f) 
                    
                    base = os.path.basename(f)
                    
                    rawwordbag = self.normal_wordbag(base)
                    
                    if rawwordbag & self._imageexts != []:
                        wordbag = rawwordbag - self._imageexts
                        print wordbag,  imagefile
                        self._db [wordbag] = imagefile 
                        # for each word bag, only one image file is stored.
            
        
    def match(self, input1):
        input = normal_wordbag(input1)
        if input in self._db:
            output = self._db[input]
            return output
        
        # TODO: partial match
        return None
        

    def uncamel(self, name):
        s1 = self._first_cap_re.sub(r'\1_\2', name)
        return self._all_cap_re.sub(r'\1_\2', s1).lower()


if __name__ == '__main__':
    
    imagedb = ImageDb()
    print imagedb._normalize_wordbag("DiSarli")
    print imagedb._normalize_wordbag("diSarli")
    print imagedb._normalize_wordbag("dArienzo")
    print imagedb._normalize_wordbag("d'Arienzo")
    print imagedb._normalize_wordbag("D'arienzo")
    
    imagedb.reset()
    
    
    d = imagedb._db
    
    for x in d:
        print x, ":", d[x]

    for s in ['Canaro', 'Di Sarli', "D'Arienzo"]:
        print s, ':', imagedb.match(s)
        
