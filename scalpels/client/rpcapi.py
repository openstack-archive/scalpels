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

    def stop_task(self, ctxt={}, uuid=None):
        self._client.cast(ctxt, "stop_task", uuid=uuid)

    def get_task(self, ctxt={}, uuid=None, fuzzy=False):
        return self._client.call(ctxt, "get_task", uuid=uuid, fuzzy=fuzzy)

    def get_latest_task(self, ctxt={}):
        return self._client.call(ctxt, "get_latest_task")

    def get_result(self, ctxt={}, uuid=None):
        return self._client.call(ctxt, "get_result", uuid=uuid)

    def get_all_results(self, ctxt={}):
        return self._client.call(ctxt, "get_all_results")

    def register_tracer(self, ctxt={}, tracer_opts=None):
        self._client.cast(ctxt, "register_tracer", tracer_opts=tracer_opts)

transport = messaging.get_transport(cfg.CONF)
rpcapi = RPCAPI(transport)
