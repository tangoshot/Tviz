'''
Created on Aug 2, 2012

@author: tolga
'''
from tviz.tandait import tandait
from StringIO import StringIO
from unidecode import unidecode

from tviz.playinglist import Playinglist
from tviz.feature_factory import TvizTandaFeatures, TvizSongFeatures,\
    UserFeatureFactory, Features




class TvizDB (object):
    '''
    Store index2features inferred from tags using defined rules for each song on the playinglist
    '''
    
    def __init__ (self, player, featurefactory):
        self._featurefactory = featurefactory
        self._player = player
        
        tagnames = self._tagnames (player, featurefactory)
        
        self._playinglist = Playinglist(player, tagnames)
        self._featuresdb = {}
        
        

    def _tagnames (self, player, featurefactory):
        playertagnames = [tagname for tagname in player.tagnames]
        
        return featurefactory.tagnames + playertagnames

    def len(self):
        return self._playinglist.len()
    
    def index2key(self, index):
        return self._playinglist.index2key(index)
    
    def playingkeys(self):
        return self._playinglist.getKeys()
    
        
    def index2features(self, index):
        assert index >= 0 
        assert index < self.len()
        
        key = self.index2key(index)
        
        # print "xxx INDEX: ", index, "KEY: ", key
        
        return self._featuresdb [key]

    def update(self):
        out = self._playinglist.update()
        
        # print "xxx **** PLAYINGLIST ****", out
        # print 'xxx LEN: \n', self._playinglist._len
        # print 'xxx INDEX: \n', self._playinglist._index
        # print 'xxx KEYS: \n', self._playinglist._keys
        # print 'xxx TAGS: \n', self._playinglist._tagdb
        
        
        # print "xxx **** PLAYINGLIST Update Status", out
        
        if out['pchanged']:
            # print 'xxx starting tags2features'
            self.tags2features()
 
        self._updateTandas()
        
        return out
        
        
    def getSong(self,index):
        return self.index2features(index)
        
    def getTanda(self,index):
        
        for tanda in self._tandas:
            if tanda.start <= index < tanda.end:
                return tanda
        
        raise Exception("index out of bound: " + index) 
    
    def currentSong(self):
        index = self._playinglist.index()
        # print "xxx CURRENT INDEX: ", index
        return self.getSong(index)

    def currentTanda(self):
        index = self._playinglist.index()
        return self.getTanda(index)

    
    def nextTanda(self):
        current = self.currentTanda()
        nextindex = current.end + 1
        if nextindex >= self.len():
            return None
        
        return self.getTanda(current.end + 1)
        
        index = self._playinglist.index
        for tanda in self._tandas:
            if tanda.start < i <= tanda.end:
                return tanda

    def tags2features(self):
        tagslist = plist = self._playinglist.tagslist() 
        factory = self._featurefactory
        
        # TODO: make this itteration overplaylist?
        for tags in tagslist:
            userfeatures = factory.tags2features(tags)
            stdfeatures = self._player.tags2features(tags)
            fdict=userfeatures
            fdict.update(stdfeatures)
            
            features = Features(fdict)
            # print 'xxx Features', features.key, repr(features)
            
            self._featuresdb.update({features.key:features}) 
        
        # print '**** tags2features ****'    
        # print 'xxx  taglist:   ', tagslist
        # print 'xxx  featuresdb:   ', self._featuresdb 
        
    def _updateTandas(self):
        
        def isbreakfn (key):
            return  self._featuresdb[key].isbreak
      
      
        self._tandas = []
        for i, j,keys in tandait(self.playingkeys(), isbreakfn):
            songfeatureslist = [self._featuresdb[key] for key in keys]
            
            # print 'yyy:', songfeatureslist
            
            tanda = TvizTanda(songfeatureslist)
            tanda.start = i
            tanda.end = j
            tanda.songs = songfeatureslist
            self._tandas.append(tanda)
        # quit()

class TvizSong(TvizSongFeatures):
    pass
    
    

class TvizTanda ():
    start = None
    end = None
    songs = None
    genre = None
    isbreak = None
    orchestra = None
    singers = []

    def __init__(self, songfeaturelist):

        # orchestra if single, else None
        orchestras = list(set([x.orchestra for x in songfeaturelist if x.orchestra]))
        if len(orchestras) == 1:
            self.orchestra = orchestras[0]
        else:
            self.orchestra = None
        
        # union of genres
        genres = list(set([x.genre for x in songfeaturelist if x.genre]))

        if genres ==[]:
            self.genre = None
        elif len(genres)==1:
            self.genre = genres[0]
        else:
            self.genre = 'Mixed'
        
        # union of isbreak but ensure that there is a single result
        isbreaks = [x.isbreak for x in songfeaturelist]
        isbreaks = set(isbreaks)
        isbreaks = list(isbreaks)
        assert len(isbreaks)==1
        self.isbreak = isbreaks[0]
        

        # union of all singers
        
        self.singers = set([])
        for song in songfeaturelist:
            newsongs = set(song.singers) - set([''])
            self.singers = self.singers or newsongs 
            
        

    def __str__(self):
        
        def cleanup (x, default=''):
            
            return unidecode(x) if x else default
        
    
        tcontext = dict(
            tgenre = cleanup(self.genre),
            tstart = self.start + 1,
            tend = self.end,
            torchestra = cleanup(self.orchestra),
            tsingers = cleanup(' & '.join(self.singers))
        )
        
        txt = '''
============================
{tgenre} Tanda: {tstart}-{tend}
============================
{torchestra} feat. {tsingers} 
----------------------------
        '''.format(**tcontext)
        
        lst = [txt]
        

        i = self.start 
        for song in self.songs:
            i = i + 1 
            genre = cleanup(song.genre, '')
            genre = '%s' % genre if genre else ''
        
            singers = ', '.join([cleanup(singer) for singer in song.singers])
            singers = 'feat. %s' % singers if singers else ''
            
            scontext = dict(
                genre = genre,
                singers = singers,
                name = cleanup(song.name),
                orchestra = cleanup(song.orchestra),
                index = i
                )
        
            txt = '{index}. {genre} {name}. {orchestra} {singers}'.format(**scontext)
            lst.append(txt)
        
        return '\n'.join(lst)

if __name__ == '__main__':

    from tviz.http_connection import HttpClient
    from settings import MySongFeatureFactory
    from jriver.mcws.player import JriverPlayer
# from tviz.playinglist import McPlayer
   
    player = JriverPlayer(user= 'mc', pwd= 'mc', port='50001')

    featurefactory = UserFeatureFactory('user_tagging')
    db = TvizDB(player = player, featurefactory= featurefactory )




    db.update()
    
    # for t in db._tandas:
    #     print t
    
    print 'Current:'
    print db.currentTanda()
           
    print ''
    print 'Next:'
    print db.nextTanda()
    
                                        
        
    
    