#!/bin/bash -x
# Author: Kun Huang <academicgareth@gmail.com>

echo "Hello, scalpels ci"
sca setup -d /opt/stack/data/scalpels/scripts

# debug messages
sudo netstat -nltp
sudo ps axf
sudo env
env

sudo iptables -A INPUT -p tcp --dport 5672
sudo iptables -L INPUT -x -n -v

echo "running load"
source /opt/stack/new/devstack/openrc admin admin
sca load --storm

sca start -a rpc
echo "running rpc tracer"
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -L INPUT -x -n -v
sudo iptables -D INPUT -p tcp --dport 5672
sca report

echo "running rabbit tracer"
sca start -a rabbit
sca report

echo "running traffic tracer"
sca start -a traffic
sca report
