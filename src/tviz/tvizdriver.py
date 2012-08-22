'''
Created on Aug 11, 2012

@author: tolga
'''
from time import sleep

from tviz.feature_factory import UserFeatureFactory, UserOptions
from tviz.http_connection import HttpClient
from tviz.tvizdb import FeatureDB, TvizTanda
from tviz.TvizRenderer import TvizRenderer
from tviz.image_matching import ImageDb

from jriver.player import JriverPlayer 


class TvizDriver:
    __client = None
    _db = None
    _player = None
    playinglist = None
    _renderer = TvizRenderer()
        
    
    def __init__(self, options_file, mapping_file):
        featurefactory = self._featurefactory = UserFeatureFactory(mapping_file)
        options = self._options = UserOptions(options_file)
        
        print "Feature Factory"
        print featurefactory
        
        print "Options:"
        print options
        
        self._imagedb= ImageDb(options)

        if options.PLAYER == 'jriver':        
            player = JriverPlayer(options.USER, 
                                  pwd = options.PWD, 
                                  port = options.PORT)
        else:
            print 'unsupport player "{player}" defined in user options file'.format(player=options.PLAYER)
            print 'Valid players are: jriver'
            quit()

        self._db = FeatureDB(player = player, 
                             featurefactory = featurefactory)
        
        self.playinglist = self._db._playinglist
        
    def index(self):
        return self.playinglist.index()


    def update(self):
        self._db.update()
        
    def renderTanda(self, tanda):
        db = self._db
        imagedb = self._imagedb

        currentsong = self._db.currentSong()
        
        self._renderer.renderTanda(tanda, currentsong, imagedb)

    def danceableTanda(self):
        tanda = self._db.currentTanda()
        
        if not tanda.isbreak:
            tanda.isnow = True
            return tanda
        
        tanda= self._db.nextTanda()
        
        if tanda:
            assert not tanda.isbreak
            tanda.isnow = False
            return tanda
                
        return None # No danceable tandas left.

def runtviz():
    
    
    while(True):
        sleep(3)    
        
        tviz = TvizDriver('user_options', 'user_tagging')
        # print tviz.index()
        
        tviz.update()
      
        tanda = tviz.danceableTanda()
        
        if not tanda:
            continue
        
        print '************************************'
        if tanda.isnow:
            print "Current Tanda"
        else:
            print "Next Tanda"
        print '************************************'
        
        tviz.renderTanda(tanda)


if __name__ == '__main__':
    
        runtviz()