from oslo_config import cfg
import oslo_messaging

class ServerControlEndpoint(object):

    #target = oslo_messaging.Target(namespace='control', version='2.0')
    target = oslo_messaging.Target(topic="test", version='2.0')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        if server:
            self.server.stop()

class TestEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='2.0')
    def test(self, ctx, arg):
        return arg

transport = oslo_messaging.get_transport(cfg.CONF)
target = oslo_messaging.Target(topic='test', server='localhost')
endpoints = [
    ServerControlEndpoint(None),
    TestEndpoint(),
]
server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                       executor='blocking')
server.start()
server.wait()
