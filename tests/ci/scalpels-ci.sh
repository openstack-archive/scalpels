#!/bin/bash -x
# Author: Kun Huang <academicgareth@gmail.com>

echo "Hello, scalpels ci"

echo "su to stack user"
su user

echo "runing rabbit tracer"
sca start -a rabbit
sca report

echo "running traffic tracer"
sca start -a traffic
sca report

echo "running rpc tracer"
sca start -a rpc
sca report
