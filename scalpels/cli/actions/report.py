#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api
def run(config):
    print "command report: %s" % config
    last_task = db_api.task_get_last()
    print "task: <%s>" % last_task.uuid
    results = []
    for ret_uuid in last_task.results:
        ret = db_api.result_get(ret_uuid)
        results.append(ret.data)
        print "result <%s>, data: %s" % (ret.uuid, ret.data)
