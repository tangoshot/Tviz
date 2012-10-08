# import web2py.gluon.template

#from rocket import Rocket
#from StringIO import StringIO
# from wsgiref.simple_server import demo_app


#def demo_app(environ,start_response):
#    stdout = StringIO()
#    
#
#    print >>stdout, \
#'''
#<HTML>
#
#<HEAD>
#<TITLE>My new webpage</TITLE>
#</HEAD>
#
#<BODY>
#(All the content of your webpage goes in here, between the <BODY> tags)
#</BODY>
#
#</HTML>
#'''    
#    start_response("200 OK", [('Content-Type','text/plain')])
#
#    return [stdout.getvalue()]

#server = Rocket(('127.0.0.1', 8006), 'wsgi', {"wsgi_app":demo_app})
#server.start()


from wsgiref.simple_server import make_server, demo_app

httpd = make_server('', 8007, demo_app)
print "Serving HTTP on port 8000..."

# Respond to requests until process is killed
httpd.serve_forever()

# Alternative: serve one request, then exit
httpd.handle_request()