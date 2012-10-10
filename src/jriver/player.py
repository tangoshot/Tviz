'''
Created on Aug 20, 2012

@author: tolga
'''
from tviz.playerAPI import PlayerInterface, PlayingListPacket
from tviz.http_connection import HttpClient

from jriver.client import JriverRequest

class JriverPlayer (PlayerInterface):
    tagnames = dict(key = 'Key', filename = 'Filename')

    base = 'MCWS/v1/'

    def __init__(self, user, pwd, port):
        self.__client = HttpClient(user = user, pwd = pwd, port = port, base = self.base)
 
    def getPlayinglistSignature(self):
        request = JriverRequest.PlayingNowListSignature()
        data = self.call(request)
        
        out = PlayingListPacket()
    
        out.len =   data['len']
        out.index = data['index']
        out.keys =  data['keys']
        
        return out

    def getPlayinglistTags(self, featuretags):
        
        request = JriverRequest.PlayingNowList(featuretags)
        tagbaglist = self.call(request)

        out = {}
        for tagbag in tagbaglist:
            key = tagbag[self.keytag()]

            for tagname in featuretags:
                if not tagname in tagbag:
                    tagbag[tagname] = ''
            
            out[key] = tagbag
        
        return out
                    
    def call(self, request):
        self.__client.call(request) 
        
        return request.response
    

