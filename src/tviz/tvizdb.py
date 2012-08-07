'''
Created on Aug 2, 2012

@author: tolga
'''

class TvizDb (object):
    def __init__ (self):
        _db = {}

    def update(self, playinglist, songfeatures):
        d[i]={}
        
        self.len = playinglist.len
        for i in range(1, self.len):
            songtags = playinglist.tags(i)
            db[i] = songfeatures(songtags)

if __name__ == '__main__':

    from tviz.http_connection import HttpClient
    from tviz.playinglist import Playinglist, McPlayer
    
    
    c = HttpClient(user= 'mc', pwd= 'mc', port='50001',base='MCWS/v1/')
    p = Playinglist(McPlayer(c))
    p.update()

    tvizdb = TvizDb(playinglist = p, featuresetup = f)

    
        
        
        
    
    