#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api
import psutil
import signal
from scalpels.cli.api import api as agent_api

LOWEST=8

def get_last_task():
    last_task = db_api.task_get_last()
    return last_task

def run(config):
    agent_api.stop_task(config)
    """
    uuid = config.get("uuid")
    last = config.get("last")

    if last and uuid:
        raise ValueError("can't assign last and uuid togther")
    elif not last and not uuid:
        task = get_last_task()
    elif last:
        task = get_last_task()
    elif uuid and len(uuid) < LOWEST:
        print "at least %d to find a task" % LOWEST
        return
    else:
        # len(uuid) > LOWEST
        task = db_api.task_get(uuid, fuzzy=True)

    print "command stop: %s" % config
    print "task: <%s>" % task.uuid
    for pid in task.pids:
        p = psutil.Process(int(pid))
        p.send_signal(signal.SIGINT)
    """
