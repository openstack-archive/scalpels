#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import prettytable

from scalpels.client import api

agent_api = api.api


def run(config):
    tracers = agent_api.get_tracer_list()
    t = prettytable.PrettyTable(["tracer", "tracer template",
                                 "is running", "pid"])
    for tr in tracers:
        t.add_row([tr["name"], tr["tpl"], tr["running"], tr["pid"]])
    print t
