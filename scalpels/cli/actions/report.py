#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api
from prettytable import PrettyTable
from mako.template import Template
from mako.lookup import TemplateLookup
from scalpels import templates
import os


def pprint_result(result):
    print "<task %s>" % result.uuid
    t = PrettyTable(["timestamp", "%s (%s)" % (result.name, result.unit)])
    for data in result.data:
        t.add_row([data[0], data[1][:100]])
    print t

LOWEST=8

def get_last_task():
    last_task = db_api.task_get_last()
    return last_task

def generate_result_html(result):
    if result.rtype == "stream":
        tmpl_dir  = os.path.dirname(templates.__file__)
        lookup = TemplateLookup(directories=[tmpl_dir])
        t = lookup.get_template("line-chart.mako")
        print t.render(**result.__dict__)

def generate_multiple_result_html(results):
    tmpl_dir  = os.path.dirname(templates.__file__)
    lookup = TemplateLookup(directories=[tmpl_dir])
    t = lookup.get_template("multi-line-chart.mako")
    d = {"results": results}
    print t.render(**d)

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
    rets = []
    for ret_uuid in task.results:
        ret = db_api.result_get(ret_uuid)
        rets.append(ret)
    if config.get("html"):
        generate_multiple_result_html(rets)
    else:
        map(pprint_result, rets)
