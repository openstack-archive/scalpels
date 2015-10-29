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

def parse_rpc(out):
    """
    in:
        ts, 123.00 pkts  2312 bytes
        ...
        ...
    out:
        name: Port Traffic
        unit: pkts
        data: [(ts, 123.00), ...]

        name: Port Traffic
        unit: bytes
        data: [(ts, 2312.00), ...]
    """
    ag_name = "Port Traffic"
    pkts_ret = {"name": ag_name,
                "unit": "pkts",
                "data":[]}
    bytes_ret = {"name": ag_name,
                "unit": "bytes",
                "data":[]}
    for ts, _t in out:
        pkts, pkts_unit, bytes, bytes_unit = _t.split(" ", 3)
        pkts_ret["data"].append((ts, pkts))
        bytes_ret["data"].append((ts, bytes))

    return (pkts_ret, bytes_ret)
