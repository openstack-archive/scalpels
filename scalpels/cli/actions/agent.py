#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.cli.actions.start import agents_map
from prettytable import PrettyTable


def run(config):
    t = PrettyTable(["tracer", "tracer script"])
    for ag in agents_map:
        t.add_row([ag, agents_map[ag]])
    print t
