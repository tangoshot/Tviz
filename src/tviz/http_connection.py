'''
Created on Jul 4, 2012

@author: tolga
'''

#TODO: move to urllib2 for authorization
# http://docs.python.org/library/urllib2.html

import urllib

class HttpClient (object):
    '''Player web service.
    Provides interface to access to different player web services
    '''

    def __init__(self, protocol='http', user='', pwd='', port=None, host='localhost', base=None):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.base = base
        self.user = user
        self.pwd = pwd

    def __str__(self):
        return self.url()
        
    def url(self):
        user= self.user
        pwd= self.pwd
        port= self.port
        host= self.host
        base= self.base
        protocol= self.protocol
        
        addr= '{protocol}://{user}{pwd}{at}{host}{port}{base}'.format(
            protocol=protocol,
            user=user if user else '',
            pwd= ':' + pwd if pwd and user else '',
            at= '@' if user else '',
            host=host,
            port=':'+port if port else '',
            base='/'+base if base else ''
        )
        return addr

    def call(self, request):        
        command = self.url() + request.query()

        self.lastcall = command
        # Open Socket
        try:
            socket = urllib.urlopen(command)
        except:
            raise Exception("Failed response for: " + command)
        try:
            request.receive(socket)
        except:
            socket.close()
            raise Exception("Cannot connect to socket")
        finally:
            socket.close()

class HttpRequest (object):
    _action= None
    _args= None
    lastcall= None
    response= None
    rawresponse= None
    _parser = None
    _reader = None
    
    def __init__(self):
        self._parser= DefaultParser()
        self._reader= DefaultReader()

    def setAction(self, action, args={}):
        self._action = action
        self._args = args
        self._clean_response()
    
    def _clean_response(self):
        self.lastcall = None
        self.rawresponse = None
        self.response = None

    def setParser(self, parser):
        self._parser= parser
    
    def parse(self, txt):
        return self._parser.parse(txt)

    def setReader(self, reader):
        self._reader= reader

    def read(self, socket):
        reader = self._reader
        return reader.read(socket)
   

    def __str__(self):
        txt= '''
        *******************************
        {action} {args}
        *******************************
        {response}
        -------------------------------
        {query}
        
        {rawresponse}
        *******************************
        '''.format(
            action = str(self._action),
            args = str(self._args),
            response = str(self.response),
            query = str(self.query()), 
            rawresponse = str(self.rawresponse))
        
        return txt
    
    def query(self):
        params = urllib.urlencode(self._args) if self._args else None
        
        return  self._action + ('?'+ params if params else '') 
       
    def call(self, server):
        self.lastcall= server.addr + self.query()
        server.call(self.lastcall) 
    
    def receive(self, socket):
        packet= self.read(socket)
        self.rawresponse= packet
        self.response = self.parse(self.rawresponse)
        
        
class DefaultParser:
    def parse(self, txt):
        return txt

class DefaultReader:
    
    def read(self, socket):
        try:
            out = socket.read()
        except:
            raise Exception( "Cannot read from socket:")
        
        return out


if __name__ == '__main__':
    c= HttpClient(user= 'mc', pwd= 'mc', port='50001',base='MCWS/v1/')
    r = HttpRequest()
    r.setAction('Alive')
    print r
    c.call(r)
    # print r
    print r.response
    
    r.setAction('Info')
    c.call(r)
    print r.response

    
