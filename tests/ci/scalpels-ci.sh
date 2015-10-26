#!/bin/bash -x
# Author: Kun Huang <academicgareth@gmail.com>

echo "Hello, scalpels ci"
sca setup -d /opt/stack/data/scalpels/scripts

# debug messages
sudo netstat -nltp
sudo ps axf
sudo env
env

echo "running load"
source /opt/stack/new/devstack/openrc admin admin
sca load --storm

echo "running rpc tracer"
sca start -a rpc
sca report

echo "running rabbit tracer"
sca start -a rabbit
sca report

echo "running traffic tracer"
sca start -a traffic
sca report
