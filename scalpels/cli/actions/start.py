#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import os
import json
from scalpels.db import api as db_api
import subprocess
import time
import signal
from scalpels.agents.base import run_agent

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
# TODO refar to pre/exec/post
agents_map = {
    "mysql": "bash %s/mysql-live.sh", #XXX doesn't work now, needs works on interapt pipeline
    "rabbit": "python %s/rbt-trace.py",
    "rpc": "bash %s/port-input-traffic.sh 5672",
    "traffic": "bash %s/device-input-traffic.sh eth0",
}

def run(config):
    print "command start: %s" % config
    agents = _parse_agents_from_args(config)
    agents |= _parse_agents_from_file(config)

    task = db_api.task_create(results=[], pids=[])

    data_dir = db_api.setup_config_get()["data_dir"].rstrip("/")
    pids = []
    for ag in agents:
        ag_exec = agents_map.get(ag) % data_dir
        if ag_exec:
            pid = run_agent(task.uuid, ag)
            pids.append(pid)

    task = db_api.task_update(task.uuid, pids=pids)
    print "task <%s> runs successfully!" % task.uuid
