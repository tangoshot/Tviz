'''
Created on Jul 4, 2012

@author: tolga
'''

#TODO: move to urllib2 for authorization
# http://docs.python.org/library/urllib2.html

import logging
import urllib2
import urllib
from xml.etree.ElementTree import ElementTree


class HttpClient (object):
    '''
    Player web service.
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
        '''
        make a service call. request is a HttpRequest object. 
        the actual reading and parsing of the return is delegated to 
        HttpRequest.getResponse function.        
        '''
            
        command = self.url() + request.encodeQuery()

        self.lastcall = command
        
        # Open Socket
        try:
            socket = urllib.urlopen(command)
        except:
            logging.error("Failed response for: " + command)
            raise

        try:
            output = request.getResponse(socket)
        except:
            logging.error("Cannot connect to socket")
            print "Cannot connect to socket"
            raise
        socket.close()
        
        return output

class HttpRequest (object):

    _action= None
    _args= None
    lastcall= None
    response= None
    rawresponse= None

    def __init__(self, action, args={}):
        self._action = action
        self._args = args


    def read(self, stream):
        '''
        reads data coming from the stream (e.g. socket),
        into an internal datastructure (e.g. ElementTree, txt, ...)
        Can be overriden my more specific versions for a more specific type 
        of http request.
        '''
        try:
            data = ElementTree.parse(stream)
        except:
            data = stream.read(stream)
        except:
            raise
    
    def parse(self, data):
        '''
        parses previously data in an internal structure (e.g. ElementTree),
        into a simplified data structure, e.g. dictionary
        '''
        try:
            return data.dump
        except:
            return data


    def __str__(self):
        txt= '''
        *******************************
        {action} {args}
        *******************************
        {response}
        -------------------------------
        {encodeQuery}
        
        {rawresponse}
        *******************************
        '''.format(
            action = str(self._action),
            args = str(self._args),
            response = str(self.response),
            query = str(self.encodeQuery()), 
            rawresponse = str(self.rawresponse))
        
        return txt
      
    def sendQuery(self, server):
        self.lastcall= server.addr + self.encodeQuery()
        server.call(self.lastcall) 
    
    def getResponse(self, socket):
        logging.debug('STARTING: getting http response')
        try:    
            self.data= self.read(socket)
        except:
            logging.error("Cannot read socket: ", socket.error())
            socket.close()
            raise

        socket.close()
        
        try:
            self.response = self.parse(self.data)
        except:
            logging.error("Cannot parse data: " + repr(packet_uni))
            
        return self.response
        
    def encodeQuery(self):
        params = urllib.urlencode(self._args) if self._args else None
        
        return  self._action + ('?'+ params if params else '') 


if __name__ == '__main__':
    c= HttpClient(user= 'mc', pwd= 'mc', port='50001',base='MCWS/v1/')
    r = HttpRequest('Alive')
    print c.call(r)
    
    r = HttpRequest('Info')
    print c.call(r)

    
