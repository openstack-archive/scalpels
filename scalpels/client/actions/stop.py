#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client.api import api as agent_api
from scalpels.client.actions.start import _parse_agents_from_args


def run(config):
    print "command stop: %s" % config
    if config["uuid"] and config["agent"]:
        raise ValueError("")
    elif config["uuid"]:
        task = agent_api.try_get_task_from_config(config)
        agent_api.stop_task(task["uuid"])
    elif config["agent"]:
        agents = _parse_agents_from_args(config)
        agent_api.stop_tracers(agents)
