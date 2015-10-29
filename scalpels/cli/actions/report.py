#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api
from prettytable import PrettyTable


def pprint_result(result):
    t = PrettyTable(["timestamp", "%s(%s)" % (result.name, result.unit)])
    for data in result.data:
        t.add_row([data[0], data[1][:100]])
    print t

LOWEST=8

def get_last_task():
    last_task = db_api.task_get_last()
    return last_task

def run(config):
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

    print "command report: %s" % config
    print "task: <%s>" % task.uuid
    for ret_uuid in task.results:
        ret = db_api.result_get(ret_uuid)
        pprint_result(ret)
