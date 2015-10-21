#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api

def run(config):
    print "command start: %s" % config
    data = [config]
    rets = []
    ret = db_api.result_create(data)
    rets.append(ret.uuid)
    task = db_api.task_create(rets)
    print "task: %s runs successfully!" % task.uuid
    return
