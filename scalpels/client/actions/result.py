#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.client.utils import generate_multiple_result_html
from scalpels.client.utils import pprint_result
from scalpels.client.utils import generate_result_html
from scalpels.client.api import api as agent_api

def run(config):
    """
    uuid: pprint it
    list: pprint all
    uuid and html: generate_result_html
    list and html: generate_multiple_result_html
    """
    if config.get("list"):
        rets = agent_api.get_all_results()
        if config.get("html"):
            generate_multiple_result_html(rets)
        elif config.get("short"):
            for ret in rets:
                print ret["uuid"]
        else:
            map(pprint_result, rets)
    elif config.get("uuid"):
        ret = agent_api.get_result(config["uuid"])
        if config.get("html"):
            generate_result_html(ret)
        else:
            pprint_result(ret)
