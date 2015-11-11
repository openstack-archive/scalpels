#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client.api import api as agent_api
from scalpels.client.utils import generate_multiple_result_html
from scalpels.client.utils import pprint_result


def run(config):
    task = agent_api.try_get_task_from_config(config)

    print "reporting task: <%s>" % task["uuid"]
    rets = []
    for ret_uuid in task["results"]:
        ret = agent_api.get_result(ret_uuid)
        rets.append(ret)
    if config.get("html"):
        generate_multiple_result_html(rets)
    else:
        map(pprint_result, rets)
