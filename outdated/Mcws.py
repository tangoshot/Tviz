#from tviz.PlayerWebService import PlayerWebService
#from McwsResponseParser import McwsXMLParser as Parser


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#				Constants
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Mcws (PlayerWebService):
    '''
    Media Center Web Service
    maintains connection and access to jriver media center player.
    '''
    DEFAULT_TIMEOUT= 50
    MSERVER_BASE= '/MCWS/v1/'
        


                
if __name__ == '__main__':

    mcws = Mcws(port=   '48105',
                user=   'mc', 
                pwd=    'mc', 
                server= 'localhost', 
                base=   'MCWS/v1' )
    
    print mcws.alive()
    print mcws.info()
    print mcws.playlists()
