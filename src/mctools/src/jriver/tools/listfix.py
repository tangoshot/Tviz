#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%                   Todo
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#% replace invalid characters: \/?><|"*:
#
#
import re
from tviz.http_connection import HttpClient
from jriver.mcws.request import JriverRequest
from copy import deepcopy
from os.path import join, dirname, exists
from os import makedirs
from shutil import rmtree


SAVED_PARENT_PATHS = [
    # 'UnitTest\\'
    '#### DJ ####\\____ TANDAS ____\\' ,
    '#### DJ ####\\____ EVENTS ____\\' 
    ]

BASE_PLAYLIST_OUTPUT = 'c:\Testbed\ListFix_Playlists'

OLD_PLAYLIST_OUTPUT = join(BASE_PLAYLIST_OUTPUT, 'OLD') 
NEW_PLAYLIST_OUTPUT = join(BASE_PLAYLIST_OUTPUT, 'NEW')


INSTALL_DRIVE = 'C:'

TAG_KEY = 'Key'
TAG_FILENAME = 'Filename'
TAG_STACKTOP = 'Stack Top'
TAG_NAME = 'Name'

class Counters:
    def __init__(self):
        self.playlists = 0
        self.files = 0
        self.top = 0
        self.single = 0
        self.updates = 0
        self.errors = 0
    
    def add(self, c):
        self.playlists += c.playlists
        self.files += c.files
        self.top += c.top
        self.single += c.single
        self.updates += c.updates
        self.errors += c.errors

       
    def __str__(self):
        return "%s playlists [%s update + %s singles +  %s top = %s totals / %s errors]" % (
            self.playlists, 
            self.updates,
            self.single,
            self.top,
            self.files, 
            self.errors)
            


def genPlaylists (client):
    response = client.call(JriverRequest.Playlists())
    assert response['status'] == True

    playlists = response['playlists']
    
    for p in playlists:
        id = p['ID']
        path = p['Path']
        if p ['Type'] != 'Playlist':
            continue
        for base in SAVED_PARENT_PATHS:
            if path.startswith(base):
                yield dict(id=id,path=path,relpath=path.replace(base,''))

def song(feature):
    if feature in song:
        song[feature]
    else:
        return ''

def getPlaylistChanges(client, id):
    counters = Counters()
    
    old_playlist = getPlaylist(client, id)
    for song in old_playlist:
        
        if TAG_FILENAME in song:
            song[TAG_FILENAME] = song[TAG_FILENAME].replace('(Install Drive):', INSTALL_DRIVE)
        else:
            counters.errors += 1
    
    new_playlist = deepcopy(old_playlist)
    
    changed = False
    for song in new_playlist:
        counters.files += 1
        
        if (not TAG_STACKTOP in song) or (song[TAG_STACKTOP] == '-1'):
            # not stacked
            counters.single += 1
            continue
        if song[TAG_STACKTOP] == song[TAG_KEY]:
            # already stack top
            counters.top += 1
            continue
        if song[TAG_STACKTOP] != song[TAG_KEY]:
            song[TAG_KEY] == song[TAG_STACKTOP]
            counters.updates += 1
            changed=True
            
    return dict(old=old_playlist, new=new_playlist, counters=counters)
        

def getPlaylist(client, id):
    request = JriverRequest.Playlist(id=id, fields=[TAG_STACKTOP, TAG_FILENAME, TAG_NAME])
    out = client.call(request)
    return out

def writePlaylist(path, playlist):
    dir = dirname(path)
        
    if not exists(dir):        
        makedirs(dir)
    
    stream = open(path, 'w')
    for song in playlist:
        if TAG_FILENAME in song:
            data = song[TAG_FILENAME].encode('utf-8')
        else:
            # print "SONG: ", song
            data = '# %s' % (song[TAG_NAME].encode('utf-8'))
    
        stream.write(data)
        stream.write('\n')
    stream.close()

def listfix():
    if exists(BASE_PLAYLIST_OUTPUT):
        rmtree(BASE_PLAYLIST_OUTPUT)

    client = HttpClient(user= 'mc', pwd= 'mc', port='48105',base='MCWS/v1/')

    COUNTERS = Counters()

    for p in genPlaylists(client):
        COUNTERS.playlists += 1
        
        id = p['id']
        path = p['path']
        

        p = getPlaylistChanges(client, id)
        c = p['counters']
        
        COUNTERS.add(c)
        if c.updates or c.errors:
            print "%s. %s (%s) [%s updates + %s singles + %s top = %s totals / %s errors ]" % (
                   COUNTERS.playlists, path, id, 
                   c.updates, c.single, c.top, 
                   c.files, 
                   c.errors)
        

        
        
        writePlaylist(join(OLD_PLAYLIST_OUTPUT+'.m3u', path), p['old'])
        writePlaylist(join(NEW_PLAYLIST_OUTPUT+'.m3u', path), p['new'])
        
    print '=============================='
    print '         SUMMARY'
    print '=============================='
    print str(COUNTERS)

if __name__ == '__main__':
    listfix()
