#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client.api import api as agent_api
from scalpels.client.actions.start import _parse_agents_from_args


def run(config):
    print "command stop: %s" % config
    if config["uuid"] and config["agent"]:
        raise ValueError("Can't stop both a task and a tracer")
    elif config["agent"]:
        agents = _parse_agents_from_args(config)
        agent_api.stop_tracers(agents)
    else:
        # no tracers are specified so trying to find a task
        task = agent_api.try_get_task_from_config(config)
        agent_api.stop_task(task["uuid"])
