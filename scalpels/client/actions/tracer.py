#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client.api import api as agent_api
from prettytable import PrettyTable


def run(config):
    tracers = agent_api.get_tracer_list()
    t = PrettyTable(["tracer", "tracer template", "is running"])
    for tr in tracers:
        t.add_row([tr["name"],tr["tpl"],tr["running"]])
    print t
