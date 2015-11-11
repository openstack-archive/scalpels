#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client.api import api as agent_api


def run(config):
    print "command stop: %s" % config

    task = agent_api.try_get_task_from_config(config)
    agent_api.stop_task(task["uuid"])
