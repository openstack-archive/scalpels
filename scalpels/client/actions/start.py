#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import json
import os

from scalpels.client import api


agent_api = api.api


def _parse_agents_from_args(config):
    parsed_agents = set()
    if config.get("agent") is None:
        return parsed_agents
    for ag in config.get("agent"):
        parsed_agents |= set(ag.split(","))
    config.update({"agent": parsed_agents})
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


def run(config):
    print "command start: %s" % config
    agents = _parse_agents_from_args(config)
    agents |= _parse_agents_from_file(config)
    agent_api.start_tracers(agents)
