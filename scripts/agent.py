#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import subprocess
import psutil
import sys
from scalpels.db import api as db_api
from copy import deepcopy as copy

"""
python <path-to-dir>/agent.py <uuid> mysql
"""

def read_from_ag(ag):
    # wrong impl. here, need read from config or db instead
    from scalpels.cli.actions.start import agents_map
    return agents_map.get(ag)

if __name__ == "__main__":
    task_uuid, ag = sys.argv[1], sys.argv[2]
    cmd = read_from_ag(ag)

    worker = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    out = []
    try:
        while True:
            t = worker.stdout.readline()
            if not len(t):
                break
            out.append(t.strip())
    except KeyboardInterrupt:
        pass
    # psutil is much more professional... I have to use it instead
    # this kill is to script process
    worker_p = psutil.Process(worker.pid)
    worker_p.kill()
    task = db_api.task_get(task_uuid)
    results = copy(task.results)
    results.append(out)
    db_api.task_update(task_uuid, results=results)
