import oslo_messaging as messaging
from oslo_config import cfg

class RPCAPI(object):

    def __init__(self, transport):
        target = messaging.Target(topic='test', version='1.0')
        self._client = messaging.RPCClient(transport, target)

    def tracer_list(self, ctxt={}):
        return self._client.call(ctxt, "tracer_list")

    def start_tracers(self, ctxt={}, tracers=None):
        self._client.cast(ctxt, "start_tracers", tracers=tracers)

    def stop_task(self, ctxt={}):
        self._client.cast(ctxt, "stop_task")

transport = messaging.get_transport(cfg.CONF)
rpcapi = RPCAPI(transport)
