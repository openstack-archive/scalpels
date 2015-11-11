#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.cli.api import api as agent_api


def run(config):
    task = agent_api.try_get_task_from_config(config)

    print "stopping task: <%s>" % task["uuid"]
    agent_api.stop_task(task["uuid"])
