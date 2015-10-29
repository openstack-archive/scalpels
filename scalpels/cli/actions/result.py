#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api
from scalpels.cli.actions import report

def run(config):
    if config.get("list"):
        rets = db_api.get_all_results()
        for ret in rets:
            report.pprint_result(ret)
