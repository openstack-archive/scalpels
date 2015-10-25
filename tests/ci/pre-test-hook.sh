#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>

localrc_path=$BASE/new/devstack/localrc
echo "DEVSTACK_GATE_TIMEOUT=120" >> $localrc_path
echo "DEVSTACK_GATE_NEUTRON=1" >> $localrc_path
echo "DEVSTACK_GATE_NEUTRON_DVR=1" >> $localrc_path
