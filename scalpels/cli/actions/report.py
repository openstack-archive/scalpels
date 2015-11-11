#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.cli.api import api as agent_api
from prettytable import PrettyTable
from mako.lookup import TemplateLookup
from scalpels import templates
import os


def pprint_result(result):
    print "<result %s>" % result["uuid"]
    t = PrettyTable(["timestamp", "%s (%s)" % (result["name"], result["unit"])])
    for data in result["data"]:
        t.add_row([data[0], data[1][:100]])
    print t

LOWEST=8

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
        task = agent_api.get_latest_task()
    elif last:
        task = agent_api.get_latest_task()
    elif uuid and len(uuid) < LOWEST:
        print "at least %d to find a task" % LOWEST
        return
    else:
        # len(uuid) > LOWEST
        task = agent_api.get_task(uuid, fuzzy=True)

    print "command report: %s" % config
    print "task: <%s>" % task["uuid"]
    rets = []
    for ret_uuid in task["results"]:
        ret = agent_api.get_result(ret_uuid)
        rets.append(ret)
    if config.get("html"):
        generate_multiple_result_html(rets)
    else:
        map(pprint_result, rets)
