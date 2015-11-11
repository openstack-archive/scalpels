#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from mako.lookup import TemplateLookup
from prettytable import PrettyTable
from scalpels import templates
import os

UUID_LOWEST_SUPPORT = 8

# TODO this map should be saved in a config file
# TODO refar to pre/exec/post
tracers_map = {
    "mysql": "bash %s/mysql-live.sh", #XXX doesn't work now, needs works on interapt pipeline
    "rabbit": "python %s/rbt-trace.py",
    "rpc": "bash %s/port-input-traffic.sh 5672",
    "traffic": "bash %s/device-input-traffic.sh eth0",
    "oslolock": "stap %s/oslo-lock.stp", # with sudo, need add current user to stapdev group
    "modelsave": "stap %s/model-save.stp", # with sudo, need add current user to stapdev group
    "sqlaexec": "stap %s/sqla-exec.stp", # with sudo, need add current user to stapdev group
    "rpccount": "stap %s/rpc-count.stp", # with sudo, need add current user to stapdev group
}


def generate_result_html(result):
    if result["rtype"] == "stream":
        tmpl_dir  = os.path.dirname(templates.__file__)
        lookup = TemplateLookup(directories=[tmpl_dir])
        t = lookup.get_template("line-chart.mako")
        print t.render(**result)

def generate_multiple_result_html(results):
    tmpl_dir  = os.path.dirname(templates.__file__)
    lookup = TemplateLookup(directories=[tmpl_dir])
    t = lookup.get_template("multi-line-chart.mako")
    d = {"results": results}
    print t.render(**d)

def pprint_result(result):
    print "<result %s>" % result["uuid"]
    t = PrettyTable(["timestamp", "%s (%s)" % (result["name"], result["unit"])])
    for data in result["data"]:
        t.add_row([data[0], data[1][:100]])
    print t
