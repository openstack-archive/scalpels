#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import subprocess
from scalpels.db import api as db_api

data_dir = db_api.setup_config_get()["data_dir"].rstrip("/")
def run_agent(task_uuid, ag):
    """
    python <path-to-dir>/agent.py <uuid> mysql
    """
    cmd = "python %s/agent.py %s %s" % (data_dir, task_uuid, ag)
    ag = subprocess.Popen(cmd.split())
    return ag.pid
