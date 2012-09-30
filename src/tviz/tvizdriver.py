'''
Created on Aug 11, 2012

@author: tolga
'''
from time import sleep

from tviz.feature_factory import UserFeatureFactory, UserOptions
from tviz.http_connection import HttpClient
from tviz.tvizdb import TvizDB, TvizTanda
from tviz.TvizRenderer import TvizRenderer
from tviz.image_matching import ImageDb

from jriver.player import JriverPlayer 



class TvizDriver:
    TVIZ_MODE_OFF = 0
    TVIZ_MODE_TANDA = 1
    TVIZ_MODE_MESSAGE = 2

    playinglist = None

    __client = None
    _db = None
    _player = None
    _renderer = TvizRenderer()
    
    def __init__(self, options_file='config', widget=None):
        self.mode = self.TVIZ_MODE_OFF
        self.message = ''
        
        options = self._options = UserOptions(options_file)
        featurefactory = self._featurefactory = UserFeatureFactory(options.PROFILE)
        
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

        self._db = TvizDB(player = player, 
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

    def renderMessage(self, message):
        self._renderer.renderMessage(message)


    def danceableTanda(self):
        tanda = self._db.currentTanda()
        print tanda
        
        if not tanda.isbreak:
            tanda.isnow = True
            return tanda
        
        tanda= self._db.nextTanda()
        
        if tanda:
            assert not tanda.isbreak
            tanda.isnow = False
            return tanda
                
        return None # No danceable tandas left.

    def run(self):
         
        while(self.mode != self.TVIZ_MODE_OFF):

            print "xxx RUN MODE: " + str(self.mode)
            print "xxx MESSAGE: " + self.message

            sleep(3)    
            
            # print tviz.index()
            
            if self.mode == self.TVIZ_MODE_TANDA:
                self.update()
      
                tanda = self.danceableTanda()
                
                if not tanda:
                    continue
                
                print 
                print '************************************'
                if tanda.isnow:
                    print "Current Tanda"
                else:
                    print "Next Tanda"
                print '************************************'
                
                print tanda
                print 
            
                self.renderTanda(tanda)
                
            if self.mode == self.TVIZ_MODE_MESSAGE:
                print "rendering : " + self.message 
                self.renderMessage(self.message)
                
        
    def setMode(self, mode):
        assert mode in [
            self.TVIZ_MODE_OFF,
            self.TVIZ_MODE_MESSAGE,
            self.TVIZ_MODE_TANDA]
        
        self.mode = mode

    def setMessage(self,message):
        print "xxx Setting message: " + message
        self.message = message


if __name__ == '__main__':
        tviz = TvizDriver('config')
        tviz.run(tviz.TVIZ_MODE_TANDA)
        