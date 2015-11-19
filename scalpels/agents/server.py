from oslo_config import cfg
import oslo_messaging
from scalpels.db import api as db_api
from scalpels.agents.base import run_agent
import psutil
import signal
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

class ServerControlEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        if server:
            self.server.stop()

class TracerEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    def tracer_list(self, ctx):
        tracers = db_api.tracer_list()
        ret = list()
        for tr in tracers:
            ret.append({"name":tr.name,
                        "tpl":tr.template,
                        "running":tr.is_running,
                        "pid":tr.pid})
        return ret

    def start_tracers(self, ctx, tracers):
        all_tr = self.tracer_list(ctx)
        running_tr = map(lambda t:t["name"], filter(lambda t:t["running"], all_tr))
        task = db_api.task_create(results=[], pids=[])

        pids = []
        for tr in tracers:
            if tr in running_tr:
                LOG.info("%s is running, skipped" % tr)
            else:
                pid = run_agent(task.uuid, tr)
                LOG.debug("saving pid %s" % pid)
                self.set_tracer_pid(ctx, tr, pid)
                pids.append(pid)

        task = db_api.task_update(task.uuid, pids=pids)
        print "[LOG] task <%s> runs successfully!" % task.uuid

    def register_tracer(self, ctx, tracer_opts):
        db_api.register_tracer(name=tracer_opts["name"], template=tracer_opts["tpl"])
        print "[LOG] registering tracer %(name)s: %(tpl)s" % tracer_opts

    def set_tracer_stat(self, ctx, tracer, running):
        running=bool(running)
        print "[LOG] setting tracer: %s running: %s" % (tracer, running)
        db_api.tracer_update(tracer, running=running)

    def set_tracer_pid(self, ctx, tracer, pid):
        db_api.tracer_update(tracer, pid=pid)

class TaskEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    def stop_task(self, ctx, uuid):
        print "[LOG] stopping task: %s" % uuid
        task = db_api.task_get(uuid)
        for pid in task.pids:
            print "[LOG] interupt process %s" % pid
            p = psutil.Process(int(pid))
            p.send_signal(signal.SIGINT)

    def get_task(self, ctx, uuid, fuzzy):
        print "[LOG] reading task: %s" % uuid
        task = db_api.task_get(uuid, fuzzy)
        # TODO object
        return {"uuid":task.uuid,
                "results":task.results,}

    def get_latest_task(self, ctx):
        task = db_api.task_get_last()
        print "[LOG] reading latest task: %s" % task.uuid
        # TODO object
        return {"uuid":task.uuid,
                "results":task.results,}

class ResultEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    def get_result(self, ctx, uuid):
        print "[LOG] reading result: %s" % uuid
        ret = db_api.result_get(uuid)
        # TODO object
        return {
                "id":ret.id,
                "uuid":ret.uuid,
                "name":ret.name,
                "unit":ret.unit,
                "data":ret.data,
                "rtype":ret.rtype,
               }

    def get_all_results(self, ctx):
        print "[LOG] reading all results"
        rets = db_api.get_all_results()
        # TODO object
        return [{"id":ret.id,
                "uuid":ret.uuid,
                "name":ret.name,
                "unit":ret.unit,
                "data":ret.data,
                "rtype":ret.rtype} for ret in rets]

class ConfigEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')
    def update_config(self, ctx, data_opts):
        db_api.update_config(data_opts)

    def get_config(self, ctx):
        return db_api.get_config()

transport = oslo_messaging.get_transport(cfg.CONF)
target = oslo_messaging.Target(topic='test', server='localhost')
endpoints = [
    ServerControlEndpoint(None),
    TracerEndpoint(),
    TaskEndpoint(),
    ResultEndpoint(),
    ConfigEndpoint(),
]
server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                       executor='blocking')
