import os

from twisted.application import service, internet, strports
from twisted.internet import reactor

from twisted.web import wsgi
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.websockets import WebSocketsResource, lookupProtocolForFactory

from twisted_store.factories import StoreFactory
from twisted_store.resources import HttpStore, StaticFileScanner
from twisted_store.wsgi import WsgiRoot
from twisted.python.threadpool import ThreadPool

from django.core.handlers.wsgi import WSGIHandler



shared_messages = {}

resource = HttpStore(shared_messages)
factory = Site(resource)
ws_resource = WebSocketsResource(lookupProtocolForFactory(resource.wsFactory))

root = Resource()
root.putChild("",resource) #the http protocol is up at /
root.putChild("ws",ws_resource) #the websocket protocol is at /ws

application = service.Application("storeserver")
#internet.TCPServer(1025, Site(root)).setServiceParent(application) # HTTP method
# Disabled HTTP, using HTTPS only.
strports.service(
    'ssl:1025:privateKey=ssl/rapidssl_privatekey_2015.key:certKey=ssl/rapidssl_publickey_2015.crt',
    Site(root),
    ).setServiceParent(application)

#serving django over wsgi
# Create and start a thread pool,
wsgiThreadPool = ThreadPool()
wsgiThreadPool.start()

django_application = WSGIHandler()
django_resource = wsgi.WSGIResource(reactor, wsgiThreadPool, django_application)

django_root = WsgiRoot(django_resource)
project_dir = os.getcwd()

internet.TCPServer(8000, Site(django_root)).setServiceParent(application)
