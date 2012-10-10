
#TODO: player API should be described in detail.
#TODO: make player client instantiation part of the player API

class PlayingListPacket (object):
    '''Interface'''

    def __str__(self):
        return  "len: " + str(self.len) + "\n" + \
                "index: " + str(self.index) + "\n" + \
                "keys: " + str(self.keys) + "\n"

class PlayerCommon:

    def keytag (self):
        return self.tagnames['key']
    
    
    def tags2features(self, tags):
        out = {}
        for featurename in self.tagnames:
            tagname = self.tagnames[featurename]
            out[featurename] = tags[tagname]
        return out
    

class PlayerInterface(PlayerCommon):
    '''Interface to a player'''

    tagnames = dict(key = '_DUMMY_', filename = '_DUMMY_')
 
    def getPlayinglistTags(self, featuretags):
        '''
        returns a dictionary that maps tags (e.g. Artist) to values
        '''
        raise Exception("getPlayinglistTags Interface must be implemented for: " + self)
    
    def getPlayinglistSignature(self):
        ''' 
        collects basic playinglist data
        returns PlayingListPacket obj.
        '''
        raise Exception( "getPlayinglistSignature Interface must be implemented for: " + self)


