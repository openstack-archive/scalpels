#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api
def run(config):
    print "command setup: %s" % config
    if config["force"]:
        db_api.db_drop()
        db_api.db_create()
    else:
        db_api.db_create()
