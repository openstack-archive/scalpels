#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client.actions.start import _parse_agents_from_args  # noqa
from scalpels.client import api
from scalpels.client import utils


agent_api = api.api


def run(config):
    if config["uuid"] and config["agent"]:
        raise ValueError("Can't stop both a task and a tracer")
    elif config["agent"]:
        req_tr = _parse_agents_from_args(config)
        all_tr = {t["name"]: t for t in agent_api.get_tracer_list()}
        for tr in req_tr:
            for ret_uuid in all_tr[tr]["results"]:
                ret = agent_api.get_result(ret_uuid)
                utils.pprint_result(ret)
    else:

        task = agent_api.try_get_task_from_config(config)

        print "reporting task: <%s>" % task["uuid"]
        rets = []
        for ret_uuid in task["results"]:
            ret = agent_api.get_result(ret_uuid)
            rets.append(ret)
        if config.get("html"):
            utils.generate_multiple_result_html(rets)
        else:
            map(utils.pprint_result, rets)
