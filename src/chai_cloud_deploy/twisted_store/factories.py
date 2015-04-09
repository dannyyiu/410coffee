from twisted.internet.protocol import Factory

from twisted_store.protocols import WebsocketStore

class StoreFactory(Factory):
    protocol = WebsocketStore
    clients = []
    messages = {}
