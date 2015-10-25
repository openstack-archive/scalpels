#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>

echo "hello, pre-test-hook"

echo "runing rabbit tracer"
sca start -a rabbit
sca report

echo "running traffic tracer"
sca start -a traffic
sca report

echo "running rpc tracer"
sca start -a rpc
sca report
