'''
Created on Aug 20, 2012

@author: tolga
'''
from tviz.playinglist import Player, PlayingListPacket
from tviz.http_connection import HttpClient

from jriver.client import JriverRequest

class JriverPlayer (Player):
    tagnames = dict(key = 'Key')
    keytag = tagnames['key']

    base = 'MCWS/v1/'

    def __init__(self, user, pwd, port):
        self.__client = HttpClient(user = user, pwd = pwd, port = port, base = self.base)
           
    def call(self, request):
        self.__client.call(request) 
        
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

    def getPlayinglistTags(self, featuretags):
        keytag = self.tagnames['key']
        
        request = JriverRequest()
        request.playingnowlist(featuretags)
        tagbaglist = self.call(request)

        out = {}
        for tagbag in tagbaglist:
            key = tagbag[keytag]

            for tagname in featuretags:
                if not tagname in tagbag:
                    tagbag[tagname] = ''
            
            out[key] = tagbag
        
        return out

