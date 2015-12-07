#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import signal
import subprocess
import sys
import time

import psutil
from tooz import coordination

from scalpels.agents import base
from scalpels.client import api
from scalpels.db import api as db_api

"""
example:
    sca-tracer <uuid> mysql
TODO:
    add help (-h) message
    config key-word arguments for each tracer
"""

agent_api = api.api
worker_pid = None
task_uuid = None
out = None
ag = None


def read_from_ag(ag):
    # wrong impl. here, need read from config or db instead
    config = agent_api.get_config()
    tracers = agent_api.get_tracer_list()
    for tr in tracers:
        if tr["name"] == ag:
            return tr["tpl"] % config
    raise ValueError("tracer %s is not found" % ag)


def handle_int(signal, frame):
    stop_tracer()
    save_result_to_task()
    agent_api.set_tracer_pid(ag, pid=-1)
    agent_api.set_tracer_stat(ag, running=False)
    sys.exit(0)


def stop_tracer():
    global worker_pid
    # psutil is much more professional... I have to use it instead
    # this kill is to script process
    worker_p = psutil.Process(worker_pid)
    worker_p.send_signal(signal.SIGINT)


def save_result_to_task():
    global task_uuid
    global out
    parse_func = getattr(base, "parse_%s" % ag)

    # TODO(kun) file lock is okay in localhost, here need redis for distributed
    # lock istead
    co = coordination.get_coordinator("file:///tmp", b"localhost")
    co.start()
    lock = co.get_lock("task_update_lock")
    with lock:
        for ret in parse_func(out):
            ret = db_api.result_create(**ret)
            print "[LOG] appending result with id %s" % ret.uuid
            db_api.task_append_result(task_uuid, ret.uuid)
            db_api.tracer_append_result(ag, ret.uuid)
        print "[LOG] update tas with result %s" % task_uuid
        time.sleep(2)
    co.stop()


def main():
    global worker_pid
    global task_uuid
    global out
    global ag
    signal.signal(signal.SIGINT, handle_int)
    task_uuid, ag = sys.argv[1], sys.argv[2]
    out = []
    cmd = read_from_ag(ag)
    print "[LOG] running CMD: %s" % cmd

    worker = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    worker_pid = worker.pid
    # this time, we got the pid, so tracer is running
    agent_api.set_tracer_stat(ag, running=True)
    while True:
        t = worker.stdout.readline()

        if not len(t):
            break
        _t = (time.time(), t.strip())
        out.append(_t)


if __name__ == "__main__":
    main()
