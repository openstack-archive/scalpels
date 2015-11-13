from oslo_config import cfg
import oslo_messaging
from scalpels.db import api as db_api
from scalpels.agents.base import run_agent
import psutil
import signal

class ServerControlEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    def __init__(self, server):
        self.server = server

    def stop(self, ctx):
        if server:
            self.server.stop()

class TraceEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    def tracer_list(self, ctx):
        # TODO db_api
        # XXX ctx required?
        from scalpels.client.utils import tracers_map
        return tracers_map

    def start_tracers(self, ctx, tracers):
        task = db_api.task_create(results=[], pids=[])

        pids = []
        for tr in tracers:
            pid = run_agent(task.uuid, tr)
            print "[LOG] saving pid %s" % pid
            pids.append(pid)

        task = db_api.task_update(task.uuid, pids=pids)
        print "[LOG] task <%s> runs successfully!" % task.uuid

class TaskEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    LOWEST = 8

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

transport = oslo_messaging.get_transport(cfg.CONF)
target = oslo_messaging.Target(topic='test', server='localhost')
endpoints = [
    ServerControlEndpoint(None),
    TraceEndpoint(),
    TaskEndpoint(),
    ResultEndpoint(),
]
server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                       executor='blocking')
