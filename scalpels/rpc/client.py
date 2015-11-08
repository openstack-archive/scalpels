import oslo_messaging as messaging
from oslo_config import cfg
class TestClient(object):

    def __init__(self, transport):
        target = messaging.Target(topic='test', version='2.0')
        self._client = messaging.RPCClient(transport, target)

    def test(self, ctxt, arg):
        return self._client.call(ctxt, 'test', arg=arg)

transport = messaging.get_transport(cfg.CONF)
print TestClient(transport).test({"ctx":"this is context"}, 'ping')
