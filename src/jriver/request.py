from tviz.http_connection import HttpRequest

from jriver.reader import McwsResponseReader, McwsMplReader, McwsSignatureReader,\
    McwsItemValueReader, FieldsItemsReader


class JriverRequest:

    class Alive(McwsItemValueReader, HttpRequest):
        
        def __init__(self):
            self.setAction('Alive')

    class Info(McwsItemValueReader, HttpRequest):
    
        def __init__(self, zone= -1):
            self.setAction('Playback/Info', {'Zone': zone})


    class Playlists (FieldsItemsReader, HttpRequest):
        
        def __init__(self):
            self.setAction('Playlists/List')


    class PlayingNowListSignature(McwsSignatureReader, HttpRequest):

        def __init__(self):
          self.setAction('Playback/Playlist',{'Action': 'Serialize'})


        
    class Authenticate(McwsItemValueReader, HttpRequest):
        
        def __init__(self):
            self.setAction('Authenticate')

    class Playlist (McwsMplReader, HttpRequest):
        
        def __init__(self, id, fields=['Name','Filename']):
            fieldsstr=','.join(fields)
            
            self.setAction('Playlist/Files', {'Playlist': id,
                                                  'Fields':fieldsstr})

    class PlayingNowList(McwsMplReader, HttpRequest):

        def __init__(self, tagnames, pvalues = None):
            if tagnames == None:
                param =  {}
            else:
                pvalues = ','.join(['[%s]' % t for t in tagnames])
                param =  {'Fields' : pvalues}
            
            self.setAction('Playback/Playlist', param)

    class PlayingNowListTest(McwsMplReader, HttpRequest): # TODO:
        
        def __init__(self): 
            self.setAction('Playback/Playlist',{'Fields':'Name,Genre,Orchestra'})
            

    class FilesSearch(McwsMplReader, HttpRequest):
        
#   Files
#
#      Search
#         Perform a database search for files.
#         Parameters:
#            Query: The search string (empty returns full library) (default: )
#            Action: The action to perform with the files (MPL: return MPL playlist; Play: plays files; Serialize: return serialized file array (basically a list of file keys)). (default: mpl)
#            Shuffle: Set to 1 to shuffle the files. (default: )
#            ActiveFile: A file key to set as active (used as the file that playback starts with, etc.). (default: -1)
#            ActiveFileOnly: Set to 1 to trim the returned files to only contain the active file. (default: )
#            PlayMode: Play mode flags delimited by commas (Add: adds to end of playlist; NextToPlay: adds files in the next to play position). (default: )
#            Fields: The fields to include in an MPL (use empty to include all fields). (default: )
#            NoLocalFilenames: Set to 1 to filter out local filenames from MPL output (since they might be meaningless to a server). (default: )
#            Zone: The zone the command is targetted for. (default: -1)
#            ZoneType: The type of value provided in 'Zone' (ID: zone id; Index: zone index; Name: zone name (default: ID)
#         Response:
#         Examples:
#            Click here
        
        def __init__(self, query='', fields=''): 
            fieldstr = ','.join(fields)
            self.setAction('Files/Search',{'Query':query, 'Fields':fieldstr})


        
    ## Any query could return this or similar:
    ## TODO: <Response Information="Unknown action 'MLP'." Status="Failure" />''

    

if __name__=='__main__':

    from tviz.http_connection import HttpClient

    client = HttpClient(user= 'mc', pwd= 'mc', port='48105',base='MCWS/v1/')
    
    
    requests = [
        JriverRequest.Alive(),
        JriverRequest.Info(),
        JriverRequest.Authenticate(),     
        JriverRequest.PlayingNowListSignature(),
        JriverRequest.PlayingNowListTest(),
        JriverRequest.PlayingNowList(['Name', 'Artist']),
        JriverRequest.FilesSearch(query='Bob Dylan', fields=['Name', 'Album Artist','Stack Top'])
    ]


    for request in requests:
        print client.call(request)
    
    
