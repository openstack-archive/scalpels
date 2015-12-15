#!/bin/bash
# Author: Fei Rao <milo.frao@gmail.com>

# TODO: More port statistics will be appended later.

dev=${1:-br-int0}

rx_packages = `sudo ovs-vsctl get interface $dev statistics | awk '{print $8}' | awk -F= '{print $2}' | awk -F, '{print $1}'`
rx_bytes = `sudo ovs-vsctl get interface $dev statistics | awk '{print $2}' | awk -F= '{print $2}' | awk -F, '{print $1}'`

interval=3

trap 'break' INT
while [ 1 -eq 1 ]  ; do
    sleep $interval
    nw_rx_packages = `sudo ovs-vsctl get interface $dev statistics | awk '{print $8}' | awk -F= '{print $2}' | awk -F, '{print $1}'`
    nw_rx_bytes = `sudo ovs-vsctl get interface $dev statistics | awk '{print $2}' | awk -F= '{print $2}' | awk -F, '{print $1}'`

    python -c "print '%0.2f pkt/s %0.2f byte/s' % ((float($nw_rx_packages-$rx_packages)/int($interval), (float($nw_rx_bytes-$rx_bytes)/int($interval))))"
    packages=$nw_rx_packages
    bytes=$nw_rx_bytes
done
