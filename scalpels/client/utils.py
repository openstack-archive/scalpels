#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import os

from mako import lookup as lookup_m
import prettytable

from scalpels import templates

UUID_LOWEST_SUPPORT = 8


# TODO(kun) this map should be saved in a config file
# TODO(kun) refar to pre/exec/post
tracers_map = {
    "mysql": "bash %s/mysql-live.sh",  #XXX doesn't work now, see bug 1512276
    "rabbit": "python %s/rbt-trace.py",
    "rpc": "bash %s/port-input-traffic.sh 5672",
    "traffic": "bash %s/device-input-traffic.sh eth0",
    "oslolock": "stap %s/oslo-lock.stp",
    "modelsave": "stap %s/model-save.stp",
    "sqlaexec": "stap %s/sqla-exec.stp",
    "rpccount": "stap %s/rpc-count.stp",
}


def generate_result_html(result):
    if result["rtype"] == "stream":
        tmpl_dir = os.path.dirname(templates.__file__)
        lookup = lookup_m.TemplateLookup(directories=[tmpl_dir])
        t = lookup.get_template("line-chart.mako")
        print t.render(**result)


def generate_multiple_result_html(results):
    tmpl_dir = os.path.dirname(templates.__file__)
    lookup = lookup_m.TemplateLookup(directories=[tmpl_dir])
    t = lookup.get_template("multi-line-chart.mako")
    d = {"results": results}
    print t.render(**d)


def pprint_result(result):
    print "<result %s>" % result["uuid"]
    t = prettytable.PrettyTable(["timestamp", "%s (%s)" % (result["name"],
                                                           result["unit"])])
    for data in result["data"]:
        t.add_row([data[0], data[1][:100]])
    print t
