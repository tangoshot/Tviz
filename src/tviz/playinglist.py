# from tviz.mcws.client import defaultjriver

from jriver.client import JriverRequest
import time
from tviz.settings import IMPORTED_TAG_NAMES

'''
@author Tolga Konik
Assumes the tags do not change within a session. This increases efficiency on large lists
'''


# TODO: ask for permission for too large queries, or use a time limit?

class Playlist(object):
    '''
    database that stores a playlist
    '''
    
    _tagdb={}
    _keys=[]
    _index=-1
    _len= -1

    def current(self):
        return self._index + 1
    
    def tags(self, index):
        return self._index2tags(index)

    def keyTags(self, key):
        return self._keys(key)

    def _index2tags(self, index):
        key= self._index2key(index)
        tags = self._tagdb[key]
        return tags
        
    def _index2key(self, index):
        intindex= index - 1
        key = self._keys [intindex]
        return key

class Playinglist (Playlist):
    ''' 
    Player independent class for updating, storing, and showing data for playing songs
    '''
    
    _player = None

    def __init__(self, player):
        self._player = player

    def readTags(self):
        t1 = time.time()
        out = self._player.getPlayinglistTags()
        t2 = time.time()
        dt = t2 - t1
        
        print "Reading Tags (%.2f seconds)" % dt
        return out
    
    def readSignature(self):
        t1 = time.time()
        out = self._player.getPlayinglistSignature()
        t2 = time.time()
        dt = t2 - t1
        print "Reading Playlist (%.2f seconds)" % dt
        return out
        
    def update(self):
        
        '''
        update len/index/keys and determine if tag database requires update.

        '''
        # slow call
        sig= self.readSignature()

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
            
        return {'pchanged' : pchanged, 'tchanged': tchanged}

    

    def _update_tagdb(self):
        newtags= self.readTags()
        self._tagdb.update(newtags)

    def _playinglist_changed(self, sig):
        if sig.len != self._len:
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

    def getPlayinglistTags(self):
        ''' 
        collects basic playinglist data
        (len, current, keys)
        '''
        print "getPlayinglistTags Interface must be implemented for:", self
        raise Exception()
    
    def getPlayinglistSignature(self):
        print "getPlayinglistSignature Interface must be implemented for:", self
        raise Exception()


class McPlayer (Player):
    keytag = 'Key'

    def __init__(self, jriverclient):
        self.jriverclient = jriverclient
    
    def call(self, request):
        self.jriverclient.call(request) 
        
        return request.response
    
    def getPlayinglistSignature(self):
        request = JriverRequest()
        request.playingnowlist_signature()
        data = self.call(request)
        
        out = PlayingListPacket()
    
        out.len =   data['len']
        out.index = data['index']
        out.keys =  data['keys']
        
        return out

    def getPlayinglistTags(self):
        keytag = self.keytag
        
        request = JriverRequest()
        request.playingnowlist(IMPORTED_TAG_NAMES)
        tagbaglist = self.call(request)

        out = {}
        for tagbag in tagbaglist:
            key = tagbag[keytag]
            out[key] = tagbag
        
        return out

    # def getPlayinglistTags(self):

if __name__ == '__main__':
    from tviz.http_connection import HttpClient

    c = HttpClient(user= 'mc', pwd= 'mc', port='50001',base='MCWS/v1/')
    player = McPlayer(c)
    p = Playinglist(player)
    p.update()
    
    print "len:",       p._len
    print "keys:",      p._keys
    print "Current: ", p.current()
    print "Current Tags: ", p.tags(p.current())
