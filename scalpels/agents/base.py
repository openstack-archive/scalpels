#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import subprocess


def run_agent(task_uuid, ag):
    """Example

    python <path-to-dir>/agent.py <uuid> mysql
    """
    cmd = "sca-tracer %s %s" % (task_uuid, ag)
    ag = subprocess.Popen(cmd.split())
    return ag.pid


def _parse_traffic(out, name):
    """Example

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
    ag_name = "%s Traffic" % name
    pkts_ret = {"name": ag_name,
                "unit": "pkts",
                "data": [],
                "rtype": "stream"}
    bytes_ret = {"name": ag_name,
                 "unit": "bytes",
                 "data": [],
                 "rtype": "stream"}
    for ts, _t in out:
        pkts, pkts_unit, bytes, bytes_unit = _t.split(" ", 3)
        pkts_ret["data"].append((ts, pkts))
        bytes_ret["data"].append((ts, bytes))

    return (pkts_ret, bytes_ret)


def parse_rpc(out):
    return _parse_traffic(out, "Port")


def parse_traffic(out):
    return _parse_traffic(out, "Device")


def parse_rabbit(out):
    """Example

    in:
        ts, {u'_unique_id': u'xxx',
             u'failure': None,
             u'ending': True,
             u'result': None,
             u'_msg_id': u'xxx'}
    out:
        name: RabbitMQ
        unit: None
        data: [(ts, <msg body>), ...]
    """
    rbt_ret = {"name": "RabbitMQ",
               "unit": None,
               "rtype": "log",
               "data": out}
    return (rbt_ret, )


def _parse_count_stream(out, name):
    ret = {"name": name,
           "unit": "count",
           "rtype": "stream",
           "data": out}
    return (ret, )


def parse_oslolock(out):
    """Example

    in:
        ts, 4
        ts, 0
        ...
    out:
        name: Oslo-Lock
        unit: Count
        data: [(ts, 0), ...)
    """
    return _parse_count_stream(out, "Oslo-Lock")


def parse_modelsave(out):
    return _parse_count_stream(out, "Model-Save")


def parse_sqlaexec(out):
    return _parse_count_stream(out, "Sqlalchemy-Execute")


def parse_rpccount(out):
    return _parse_count_stream(out, "RPC-Count")
