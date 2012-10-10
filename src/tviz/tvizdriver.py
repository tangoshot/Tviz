'''
Created on Aug 11, 2012

@author: tolga
'''

import logging

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
        
        logging.info("Feature Factory: \n" + str(featurefactory))
        
        logging.info("Options:\n" + str(options))
        
        self._imagedb= ImageDb(options)

        if options.PLAYER == 'jriver':        
            player = JriverPlayer(options.USER, 
                                  pwd = options.PWD, 
                                  port = options.PORT)
        else:
            logging.error('unsupport player "{player}" defined in user options file'.format(player=options.PLAYER))
            logging.error('Valid players are: jriver')
            quit()

        self._db = TvizDB(player = player, 
                             featurefactory = featurefactory)
        
        self.playinglist = self._db._playinglist
        
    def index(self):
        return self.playinglist.index()


    def update(self):
        return self._db.update()
        
    def renderTanda(self, tanda):
        db = self._db
        imagedb = self._imagedb

        currentsong = self._db.currentSong()
        
        # print "CURRENT Tanda: ", tanda
        # print "CURRENT Song: ", currentsong
                
        self._renderer.renderTanda(tanda, currentsong, imagedb)

    def renderMessage(self, message):
        self._renderer.renderMessage(message)


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

    def run(self):
        self.mode = self.TVIZ_MODE_TANDA
        while (True):
            self.run_one()
            sleep(3)    


    def run_one(self):
        print "xxx RUN MODE: " + str(self.mode)
        # print "xxx MESSAGE: " + self.message
        
        if self.mode == self.TVIZ_MODE_OFF:
           # print "xxx Tviz off. returning control"
           return
        
        if self.mode == self.TVIZ_MODE_MESSAGE:
            self.run_one_show_message()
            return 
        
        if self.mode == self.TVIZ_MODE_TANDA:
            self.run_one_show_tanda()
                



    def run_one_show_message(self, messageparam=None):
            if messageparam:
                message = messageparam
            else:
                message = self.message
        
            logging.debug("rendering message: " + message) 
            self.renderMessage(message)
            
    def run_one_show_tanda(self):
        if self.mode == self.TVIZ_MODE_TANDA:
            
            update_result = self.update()
            # print 'xxx UPDATE results, ',update_result  
        
            tanda = self.danceableTanda()
            
            if not tanda:
                logging.info('no tanda available')
            
            if update_result['pchanged']:
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
            
                
        
    def setMode(self, mode):
        assert mode in [
            self.TVIZ_MODE_OFF,
            self.TVIZ_MODE_MESSAGE,
            self.TVIZ_MODE_TANDA]
        self.mode = mode

    def setMessage(self,message):
        self.message = message


if __name__ == '__main__':
        tviz = TvizDriver('config')
        tviz.run()
        