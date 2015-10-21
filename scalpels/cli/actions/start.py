#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api

def _parse_agent_from_config(config):
    if config.get("agent") is None:
        return config
    parsed_agents = []
    for ag in config.get("agent"):
        parsed_agents.extend(ag.split(","))
    config.update({"agent":parsed_agents})
    return config


def run(config):
    config = _parse_agent_from_config(config)
    print "command start: %s" % config
    data = [config]
    rets = []
    ret = db_api.result_create(data)
    rets.append(ret.uuid)
    task = db_api.task_create(rets)
    print "task: %s runs successfully!" % task.uuid
    return
