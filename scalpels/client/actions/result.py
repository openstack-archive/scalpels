#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client import api
from scalpels.client import utils


agent_api = api.api


def run(config):
    """Run Command

    uuid: pprint it
    list: pprint all
    uuid and html: generate_result_html
    list and html: generate_multiple_result_html
    """
    if config.get("list"):
        rets = agent_api.get_all_results()
        if config.get("html"):
            utils.generate_multiple_result_html(rets)
        elif config.get("short"):
            for ret in rets:
                print ret["uuid"]
        else:
            map(utils.pprint_result, rets)
    elif config.get("uuid"):
        ret = agent_api.get_result(config["uuid"])
        if config.get("html"):
            utils.generate_result_html(ret)
        else:
            utils.pprint_result(ret)
