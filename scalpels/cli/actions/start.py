#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import os
import json
from scalpels.db import api as db_api
import subprocess
import time

def _parse_agents_from_args(config):
    parsed_agents = set()
    if config.get("agent") is None:
        return parsed_agents
    for ag in config.get("agent"):
        parsed_agents |= set(ag.split(","))
    config.update({"agent":parsed_agents})
    return parsed_agents


def _parse_agents_from_file(config):
    parsed_agents = set()
    if config.get("file") is None:
        return parsed_agents
    fpath = config.get("file")
    if not os.path.isfile(fpath):
        return parsed_agents
    with open(fpath) as f:
        data = json.load(f)
    for ag in data["agents"]:
        parsed_agents.add(ag["name"])
    return parsed_agents

# TODO this map should be saved in a config file
agents_map = {
    "mysql": "",
    "rabbit": "",
    "traffic": "",
    "rpctraffic": "",
}

def run(config):
    print "command start: %s" % config
    agents = _parse_agents_from_args(config)
    agents |= _parse_agents_from_file(config)
    running_agents = []
    for ag in agents:
        ag_exec = agents_map.get(ag)
        if ag_exec:
            ag_p = subprocess.Popen(ag_exec, stdout=subprocess.PIPE)
            running_agents.append(ag_p)
    time.sleep(15)
    data = []
    for ag_p in running_agents:
        stdout = ag_p.communicate()[0]
        ag_p.terminate()
        data.append(stdout)
    rets = []
    ret = db_api.result_create(data)
    rets.append(ret.uuid)
    task = db_api.task_create(rets)
    print "task: %s runs successfully!" % task.uuid
    return
