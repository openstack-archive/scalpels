#!/bin/bash -x
# Author: Kun Huang <academicgareth@gmail.com>

sca-manage setup -f
sca-manage setup -d rpcport=5672 -t name=rpc -t tpl="bash %(tracer_path)s/port-input-traffic.sh %(rpcport)s"
sca-manage setup -t name=mysql -t tpl="bash %(tracer_path)s/mysql-live.sh"
sca-manage setup -t name=rabbit -t tpl="python %(tracer_path)s/rbt-trace.py"
sca-manage setup -d port=eth0 -t name=traffic -t tpl="bash %(tracer_path)s/device-input-traffic.sh %(port)s"
sca-manage setup -t name=oslolock -t tpl="stap %(tracer_path)s/oslo-lock.stp"
sca-manage setup -t name=modelsave -t tpl="stap %(tracer_path)s/model-save.stp"
sca-manage setup -t name=sqlaexec -t tpl="stap %(tracer_path)s/sqla-exec.stp"
sca-manage setup -t name=rpccount -t tpl="stap %(tracer_path)s/rpc-count.stp"
sca tracer -l
