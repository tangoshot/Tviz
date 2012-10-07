# from tviz.mcws.client import defaultjriver
import logging

from jriver.client import JriverRequest
import time
from pickle import HIGHEST_PROTOCOL


'''
@author Tolga Konik
Assumes the tags do not change within a session. This increases efficiency on large lists
'''
#TODO: Important _missing_tags is not working. Tags are not cached

# TODO: ask for permission for too large queries, or use a time limit?

class Playlist(object):
    '''
    database that stores a playlist
    '''

    def __init__(self, importedtags):
        _tagdb={}
        _keys=[]
        _index=None
        _len=None
        self.importedtags = importedtags

    def current(self):
        return self._index + 1
    
    def index(self):
        return self._index 

    # TODO: add ability to return all tags.
        
    def tagslist(self):
        # print self._keys
        return [self.keyTags(key) for key in self._keys]
    
    def currentkey(self):
        key = self._keys [self.index()]
        return key
    
    def tags(self, index):
        '''
        returns none for missing tags
        '''

        
        return self._index2tags(index)

    def keyTags(self, key):
        return self._tagdb[key]

    def _index2tags(self, index):
        key= self.natural_index2key(index)
        tags = self._tagdb [key]
        
        out = {}
        for tagname in IMPORTED_TAG_NAMES:
            out[tagname] = tags[tagname]

        return out
        
    def index2key(self, index):
        key = self._keys [index]
        return key

    def natural_index2key(self, index):
        intindex= index - 1
        key = self._keys [intindex]
        return key
    
    def getKeys(self):
        return self._keys
        

class Playinglist (Playlist):
    ''' 
    Player independent class for updating, storing, and showing data for playing songs
    '''
    
    _player = None
    

    def __init__(self, player, usertagnames):
        self._len = -1
        self._keys = []
        self._index = -1
        self._tagdb={}

        
        self._player = player
        playertags = [player.tagnames[name] for name in player.tagnames]
        self.importedtags = usertagnames + playertags
        

    def readTags(self):
        t1 = time.time()
        out = {}
        out = self._player.getPlayinglistTags(self.importedtags)
        t2 = time.time()
        dt = t2 - t1
        
        
        infostr = "Reading Tags (%.2f seconds)" % dt
        print infostr
        logging.info(infostr)
        return out
    
    def readSignature(self):
        t1 = time.time()
        out = self._player.getPlayinglistSignature()
        t2 = time.time()
        dt = t2 - t1
        infostr = "Reading Playlist (%.2f seconds)" % dt
        print infostr
        logging.info(infostr)
        
        return out
        
    def update(self):
        
        '''
        update len/index/keys and determine if tag database requires update.
        return dict:
            pchanged: True/False # playlist signature is changed

        '''
        # slow call
        sig= self.readSignature()
        # print "xxx playlist signature: ", repr(sig)
        pchanged = False # playing list is changed
        tchanged = False # tags are changed

        if self._playinglist_changed(sig):
            
            pchanged = True
            self._len = sig.len
            self._keys = sig.keys
            self._index = sig.index

            if self._missing_tags(sig):    
                # slow call
                self._update_tagdb()
                tchanged = True
            
        d= dict(pchanged= pchanged, tchanged=tchanged)
        return d

    def len(self):
        return self._len

    def _update_tagdb(self):
        newtags= self.readTags()
        self._tagdb.update(newtags)

    def _playinglist_changed(self, sig):
        if sig.len != self._len:
            return True
        if sig.index!= self._index:
            return True
        
        if sig.keys != self._keys:
            return True
        return False            

    def _missing_tags(self, sig):
        # TODO: I need to evaluate whether this shortcut creates problems.
        # for example, when the tags are changed on the fly or when new files are
        # added to the database etc.
        for key in sig.keys:
            if not key in self._tagdb:
                return True
        return False

class PlayingListPacket (object):
    '''Interface'''

    def __str__(self):
        return  "len: " + str(self.len) + "\n" + \
                "index: " + str(self.index) + "\n" + \
                "keys: " + str(self.keys) + "\n"

class Player:
    '''Interface to a player'''

    def getPlayinglistTags(self, featuretags):
        ''' 
        collects basic playinglist data
        (len, current, keys)
        '''
        raise Exception("getPlayinglistTags Interface must be implemented for: " + self)
    
    def getPlayinglistSignature(self):
        raise Exception( "getPlayinglistSignature Interface must be implemented for: " + self)

       
         
        


#class McPlayer (Player):
#    keytag = 'Key'
#
#    def __init__(self, jriverclient):
#        self.jriverclient = jriverclient
#    
#    def call(self, request):
#        self.jriverclient.call(request) 
#        
#        return request.response
#    
#    def getPlayinglistSignature(self):
#        request = JriverRequest()
#        request.playingnowlist_signature()
#        data = self.call(request)
#        
#        out = PlayingListPacket()
#    
#        out.len =   data['len']
#        out.index = data['index']
#        out.keys =  data['keys']
#        
#        return out
#
#    def getPlayinglistTags(self):
#        keytag = self.keytag
#        
#        request = JriverRequest()
#        request.playingnowlist(IMPORTED_TAG_NAMES)
#        tagbaglist = self.call(request)
#
#        out = {}
#        for tagbag in tagbaglist:
#            key = tagbag[keytag]
#
#            for tagname in IMPORTED_TAG_NAMES:
#                if not tagname in tagbag:
#                    tagbag[tagname] = ''
#            
#            out[key] = tagbag
#        
#        return out

    # def getPlayinglistTags(self):

if __name__ == '__main__':
    IMPORTED_TAG_NAMES = [        
            'Name',
            'Orchestra',
            'Genre',
            'Singer',
            'Key',
            'Subgroup']    

    from jriver.player import JriverPlayer

    player = JriverPlayer(user= 'mc', pwd= 'mc', port='50001')
    p = Playinglist(player, IMPORTED_TAG_NAMES)
    p.update()
    
    logging.debug("len:" + p._len)
    logging.debug("keys:" + p._keys)
    logging.debug("Current: " + p.current())
    logging.debug("Current Tags: " + p.tags(p.current()))
    
    # from cPickle import dump, load
    # import pickle 
    #s = open('playlistdump.txt', 'wb')
    #dump(p, s, HIGHEST_PROTOCOL)
    
    #s2 = open('playlistdump.txt', 'rb')
    #p2 = load(s2)
    # print "p2:", str(p2)
    