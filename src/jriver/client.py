from jriver import parser

from tviz.http_connection import HttpRequest, HttpClient

from jriver.parser import McwsResponseParser, McwsXmlParser, McwsMplParser,\
    McwsParser, McwsSignatureParser


class JriverRequest(HttpRequest):
   
    
    def alive(self):
        self.setAction('Alive')
        self.setParser(McwsResponseParser())
    
    def info (self, zone = -1, ):
        self.setAction('Playback/Info', {'Zone': zone})
        self.setParser(McwsResponseParser())

    def playlists (self):
        self.setAction('Playlists/List')
        self.setParser(McwsMplParser())

    def playingnowlist_signature(self):
        def f (x): 
            return x
           
        self.setAction('Playback/Playlist',{'Action': 'Serialize'})
        self.setParser(McwsSignatureParser())

    def playingnowlist(self, pvalues = None):

        if self.tagnames == None:
            param =  {}
        else:
            pvalues = ','.join(['[%s]' % t for t in self.tagnames])
            param =  {'Fields' : pvalues}
        
        self.setAction('Playback/Playlist', param)
        self.setParser(McwsMplParser())

    def playingnowlist_test(self): # TODO: 
        self.setAction('Playback/Playlist',{'Fields':'Name,Genre,Orchestra'})
        self.setParser(McwsMplParser())
        
    def authenticate(self):
        self.setAction('Authenticate')
        self.setParser(McwsResponseParser())
        
    ## Any query could return this or similar:
    ## TODO: <Response Information="Unknown action 'MLP'." Status="Failure" />''


if __name__=='__main__':

        c = HttpClient(user= 'mc', pwd= 'mc', port='50001',base='MCWS/v1/')
        
        r = JriverRequest()  

        r.playingnowlist_test()
        c.call(r)
        print r.response
        print r._args
        print r.query()
        print r.lastcall
        quit()
        
        r.alive()
        c.call(r)
        print repr(r.response)
                
        r.info()
        c.call(r)
        print repr(r.response)
        
        r.playingnowlist()
        print r._args
        c.call(r)
        print repr(r.response)
        
        r.authenticate()
        c.call(r)
        print r.response
        
        r.playingnowlist_signature()
        c.call(r)
        print r.response


        
        # print r.rawresponse