'''
Created on Jul 4, 2012

@author: tolga
'''

class AbstractPlayer:
    '''abstract player interface tviz uses to connect to return data from player'''
    
    def __init__(self):
        pass

    def get_playlist_signature(self):
        '''
        Return a string reprenting the current playlist
        used to detect changes in the current playlists without 
        needing to query the whole list.
        
        ''' 
        pass
    
    def getPlayinglist(self):
        pass
        
    def connect(self):
        pass
    
    def alive(self):
        pass
        



class SamplePlayer(AbstractPlayer):
    '''abstract player interface tviz uses to connect to return data from player'''
    
    def get_playlist_signature(self):
        return '2;key1;key2'
    
    def getPlayinglist(self):
        
        sample_playlist= [
           { 'name': 'Song Name1',
             'artist': 'Artist1',
             'genre': 'Genre1'
            },
                          
           { 'name': 'Song Name2',
             'artist': 'Artist2',
             'genre': 'Genre2'
            }]
                          
        return sample_playlist
        
    def connect(self):
        return True

