'''
Created on Aug 5, 2012

@author: tolga
'''
import os
from settings import label_image_folder, orchestra_image_folder, singer_image_folder
from tutil.string import normal_wordbag

class ImageDb():

    _imageexts = frozenset(['gif', 'jpg', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'webp'])
    _db = {}
    

    def reset(self):
        for imagefolder in [label_image_folder, orchestra_image_folder, singer_image_folder]:
            for _dir, _subdirs, files in os.walk(imagefolder):
                for f in files:
                    imagefile = os.path.join(dir,f) 
                    
                    base = os.path.basename(f)
                    
                    rawwordbag = normal_wordbag(base)
                    
                    if rawwordbag & self._imageexts != []:
                        wordbag = rawwordbag - self._imageexts
                        print wordbag,  imagefile
                        self._db [wordbag] = imagefile 
                        # for each word bag, only one image file is stored.
            
        
    def match(self, instr1):
        instr = normal_wordbag(instr1)
        if instr in self._db:
            outstr = self._db[input]
            return outstr
        
        # TODO: partial match
        return None
        



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
        
