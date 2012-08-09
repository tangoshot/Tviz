'''
Created on Aug 2, 2012

@author: tolga
'''

class TvizPlayinglist (object):
    '''
    Store features inferred from tags using defined rules for each song on the playinglist
    '''
    
    
    def __init__ (self,playinglist, featurefactory):
        
        self._playinglist = playinglist
        self._featurefactory = featurefactory
        self._featuresdb = {}

    def len(self):
        return self.playinglist.len

    def update(self):
        
        out = self._playinglist.update()
        if out.tupdated:
            self.infer()

        
    def infer(self):
        plist = self._playinglist 
        factory = self._featurefactory

        for i in range(1, self.len()):
            tags = plist.tags(i)          
            self._featuresdb[i] = factory.infer(tags) # TODO: factory.infer
            
    
    
            
class TvizSongFeatures:
    ## MISSING Instrumental marker
    
    '''
    inferred features of a song
    '''
    name = None
    orchestra = None
    singerlist = []
    genre = None
    isbreak = None
    isinstrumental = None

    def __str__ (self):
        wordlist = [   
            "name:           ", self.name, "\n", 
            "orchestra:      ", self.orchestra, "\n",
            "genre:          ", self.genre, "\n",
            "isbreak:        ", str(self.isbreak), "\n",
            "isinstrumental: ", str(self.isbreak), "\n",
            "singers:        ", str(self.singers), "\n"]
        
        return ''.join(wordlist)


class TvizTandaFeatures:
    orchestra = None
    singerlist = None
    genre = None
    isbreak = None
    # isinstrumental = None

    def __str__ (self):
        wordlist = [   
            "orchestra:      ", self.orchestra, "\n",
            "genre:          ", self.genre, "\n",
            "isbreak:        ", str(self.isbreak), "\n",
            # "isinstrumental: ", str(self.isbreak), "\n",
            "singers:        ", str(self.singers), "\n"]
        
        return ''.join(wordlist)
    
    def _merge_singleton(self, itemlist):
        itemset = frozenset(itemlist)
        if len(itemset) == 1:
            return itemset[0]
        else:
            return None
        
           
        
    
    def merge(self, tandalist):

        # orchestra if single, else None
        self.orchestra = self._merge_singleton([x.orchestra for x in tandalist])
        
        # union of genres
        self.genre = [x.genre for x in tandalist]
        
        # union of isbreak but ensure that there is a single result
        self.isbreak = self._merge_singleton([x.isbreak for x in tandalist])
        assert len([x.isbreak for x in tandalist]) == 1

        # union of all singers
        self.singers = set([])
        for x in tandalist:
            self.singers.union(set(x.singers))

        
        



if __name__ == '__main__':

    from tviz.http_connection import HttpClient
    from tviz.playinglist import Playinglist, McPlayer
    from settings import MySongFeatureFactory
   
   
    c = HttpClient(user= 'mc', pwd= 'mc', port='50001',base='MCWS/v1/')
    p = Playinglist(McPlayer(c))
        
    tvizp = TvizPlayinglist(playinglist = p, featurefactory= MySongFeatureFactory())
    tvizp.update()

    
        
        
        
    
    