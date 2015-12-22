#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>

dev=${1:-eth0}

function get_rx_packets()
{
    echo  `cat /sys/class/net/$dev/statistics/rx_packets `
}

function get_rx_bytes()
{
    echo `cat /sys/class/net/$dev/statistics/rx_bytes `
}

packages=$(get_rx_packets)
bytes=$(get_rx_bytes)

interval=3

trap 'break' INT
while [ 1 -eq 1 ]  ; do
    sleep $interval
    n_packages=$(get_rx_packets)
    n_bytes=$(get_rx_bytes)
    python -c "print '%0.2f pkt/s %0.2f byte/s' % ((float($n_packages-$packages)/int($interval), (float($n_bytes-$bytes)/int($interval))))"
    packages=$n_packages
    bytes=$n_bytes
done
