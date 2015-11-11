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
        from scalpels.cli.actions.start import agents_map
        return agents_map

    def start_tracers(self, ctx, tracers):
        print locals()
        task = db_api.task_create(results=[], pids=[])

        pids = []
        for tr in tracers:
            pid = run_agent(task.uuid, tr)
            pids.append(pid)

        task = db_api.task_update(task.uuid, pids=pids)
        print "task <%s> runs successfully!" % task.uuid

class TaskEndpoint(object):

    target = oslo_messaging.Target(topic="test", version='1.0')

    LOWEST = 8

    def get_last_task(self):
        # XXX put it tu utils?
        last_task = db_api.task_get_last()
        return last_task

    def stop_task(self, ctx):
        uuid = ctx.get("uuid")
        last = ctx.get("last")

        if last and uuid:
            raise ValueError("can't assign last and uuid togther")
        elif not last and not uuid:
            task = self.get_last_task()
        elif last:
            task = self.get_last_task()
        elif uuid and len(uuid) < self.LOWEST:
            print "at least %d to find a task" % self.LOWEST
            return
        else:
            # len(uuid) > LOWEST
            task = db_api.task_get(uuid, fuzzy=True)

        print "command stop: %s" % ctx
        print "task: <%s>" % task.uuid
        for pid in task.pids:
            p = psutil.Process(int(pid))
            p.send_signal(signal.SIGINT)

    def get_task(self, ctx, uuid, fuzzy):
        task = db_api.task_get(uuid, fuzzy)
        # TODO object
        return {"uuid":task.uuid,
                "results":task.results,}

    def get_latest_task(self, ctx):
        task = db_api.task_get_last()
        # TODO object
        return {"uuid":task.uuid,
                "results":task.results,}

    def get_result(self, ctx, uuid):
        ret = db_api.result_get(uuid)
        # TODO object
        return {
                "id":ret.id,
                "uuid":ret.uuid,
                "name":ret.name,
                "unit":ret.unit,
                "data":ret.data,
               }

transport = oslo_messaging.get_transport(cfg.CONF)
target = oslo_messaging.Target(topic='test', server='localhost')
endpoints = [
    ServerControlEndpoint(None),
    TraceEndpoint(),
    TaskEndpoint(),
]
server = oslo_messaging.get_rpc_server(transport, target, endpoints,
                                       executor='blocking')
