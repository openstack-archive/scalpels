#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>

port=$1
protocol=${2:-tcp}
chain="PREROUTING"
if [ -z "$port" ]; then
    echo "You must specify a port"
    exit 1
fi

if ! [[ "$port" =~ ^[0-9]+$ ]] ; then
    echo $port is not numberic
    exit 1
fi

if [ "$port" -ge 65536 ] || [ "$port" -le 0 ] ; then
    echo $port is not valid in 1~65535
    exit 1
fi

rule="$chain -p $protocol --dport $port"

#XXX iptables -A INPUT -p tcp --dport 5672
echo applying rule: $rule
sudo iptables -t mangle -A $rule

interval=3
packages=0
bytes=0
trap 'break' INT
while [ 1 -eq 1 ]  ; do
    sleep $interval
    n_packages=`sudo iptables -t mangle -L $chain -n -v -x | grep $port | grep $protocol | tail -n 1 | awk '{print $1}'`
    n_bytes=`sudo iptables -t mangle -L $chain -n -v -x | grep $port | grep $protocol | tail -n 1 | awk '{print $2}'`
    python -c "print '%0.2f pkt/s' % (float($n_packages-$packages)/int($interval))"
    python -c "print '%0.2f byte/s' % (float($n_bytes-$bytes)/int($interval))"
    packages=$n_packages
    bytes=$n_bytes
done

echo deleting rule: $rule
sudo iptables -t mangle -D $rule
