from gluon import *
from gluon import template
from paths import template_file, html_file
from shutil import copy
import codecs 
from gluon import P


def singerstext(SINGERS):
    if len(SINGERS) == 0:
        return ''
 
    if len(SINGERS) >= 3:
        return '; '.join(SINGERS[:-1]) + '; and ' + SINGERS[-1]

    assert len(SINGERS) in [1,2] 
    
    return ' and '.join(SINGERS)
   

class Song:
    name = None
    highlighting = 'normal'

    def __init__(self, name, highlighting=False):
        self.name = name.encode('ascii', 'xmlcharrefreplace')
        
        print name, name.__class__
        
        if highlighting:
            self.highlighting='highlighted'
        else:
            self.highlighting = 'normal'

# self.GENRE = cgi.escape(GENRE) if GENRE else ''
        
class PlayingSong:

    def __init__(self, imagedb, name, orchestra, SINGERS): 
        
        orchestra = orchestra if orchestra else ''
        singerstxt =  singerstext(SINGERS)
        
        self.artists = ' featuring '.join([ orchestra.encode('ascii', 'xmlcharrefreplace'),
                             singerstxt.encode('ascii', 'xmlcharrefreplace') ])

        imagequeries= []       
        if orchestra:
            imagequeries.append(orchestra)
        imagequeries = imagequeries + list(SINGERS) + [name]
            
        images = []
        for query in imagequeries:
            result = imagedb.find(query)
            if result:
                images.append(result)
        self.images = images
        
        
class Banner():
    def html (self):
        
        out = DIV(                  
            BR(),
            BR(),
            P( 'TangoShot.com',  
               _style="color:rgb(40,40,40);font-size:6em;font-weight:bold;"))                  
        
        return out


class TvizRenderer:
    banner = Banner()
    
    def __init__(self):
        copy(template_file('main.css'), html_file('main.css'))
        copy(template_file('index.html'), html_file('index.html'))
        
    def getSongs(self, curTanda, currentkey):
        songs = []
        for song in curTanda.songs:
            highlighting = True if song.key == currentkey else False
            songs.append(Song(name=song.name, highlighting = highlighting))
        return songs
        

    def renderTanda(self, tanda, currentsong,imagedb):
        # print curTanda

        songs = self.getSongs(tanda, currentsong.key)
        
        if tanda.orchestra:
            
            tandaorchestra = tanda.orchestra
            currentorchestra = None
        else:
            tandaorchestra = None
            currentorchestra = currentsong.orchestra
       
        playingsong = PlayingSong(imagedb, currentsong.name, currentorchestra, currentsong.singers)
                    
        tandaorchestraimage = None
        
        if tandaorchestra:
            tandaorchestraimage = imagedb.find(tandaorchestra)
        
        title = self.title(tanda.isnow, tandaorchestra, tanda.genre)
                    
        context = dict(
            title= title, 
            songs = songs,
            tandaorchestraimage = tandaorchestraimage,
            subtitle = playingsong.artists,
            playingsong_images = playingsong.images,
            XML = XML,
            isnow = tanda.isnow,
            banner = self.banner.html()
            
            )
        # print context
        self.render('basic.html', context)


    def title(self, isnow, orchestra, GENRE):
        
        isnow = '' if isnow else 'Next: '
                
        orchestra = ' {o} '.format(o = orchestra) if orchestra else '' 
        
        title = '{isnow}{orchestra}{GENRE} Tanda'.format(
             isnow=isnow,
             orchestra = orchestra,
             GENRE = GENRE )
        
        return title
                            
    
    def render(self, filename, context):

        try:
            templatetxt = open(template_file(filename), 'r').read()
        except:
            raise Exception("HtmlRenderer: Error reading: " + filename)
                    
        try:
            outputhtml = template.render(content= templatetxt, context = context)
            
        except:
            print "HtmlRenderer: Error rendering: " + filename
            raise 

        outfile = html_file('tanda.html')
        
        try:
            out = codecs.open(outfile, 'w')
            out.write(outputhtml)
            out.close()
        except:
            print "HtmlRenderer: Error writing to file: ", outfile
            

    

if __name__ == '__main__':
    

    u = u'Yuyo verde (Callej\xf3n)'
    u =  u.encode('ascii', 'xmlcharrefreplace')

    songs = [Song('song1'), Song('song2', True), Song('song3'), Song('...more...')] 
    
    context = dict(title='My Title', songs = songs, XML=XML, subtitle=u, playingsong_images=[] )

    r = TvizRenderer()
    r.render('basic.html', context)



