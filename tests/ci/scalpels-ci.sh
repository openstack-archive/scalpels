#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>

echo "Hello, scalpels ci"

echo "runing rabbit tracer"
sca start -a rabbit
sca report

echo "running traffic tracer"
sca start -a traffic
sca report

echo "running rpc tracer"
sca start -a rpc
sca report
