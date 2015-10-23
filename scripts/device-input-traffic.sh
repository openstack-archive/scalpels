#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>

dev=${1:-eth0}

packages=`cat /sys/class/net/$dev/statistics/rx_packets `
bytes=`cat /sys/class/net/$dev/statistics/rx_bytes `

interval=3

trap 'break' INT
while [ 1 -eq 1 ]  ; do
    sleep $interval
    n_packages=`cat /sys/class/net/$dev/statistics/rx_packets `
    n_bytes=`cat /sys/class/net/$dev/statistics/rx_bytes `
    python -c "print '%0.2f pkt/s' % (float($n_packages-$packages)/int($interval))"
    python -c "print '%0.2f byte/s' % (float($n_bytes-$bytes)/int($interval))"
    packages=$n_packages
    bytes=$n_bytes
done
