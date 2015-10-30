#!/bin/bash -x
# Author: Kun Huang <academicgareth@gmail.com>

echo "Hello, scalpels ci"
sca setup -d /opt/stack/data/scalpels/scripts

# debug messages
sudo netstat -nltp
sudo ps axf
sudo env
env

sudo apt-search kernel-image # find a lastest one, 3.19.0-30-generic for example
sudo apt-get install -y linux-image-3.19.0-30-generic linux-headers-3.19.0-30 linux-headers-3.19.0-30-generic
# reboot your system to ensure you are running the new kernel
codename=$(lsb_release -c | awk  '{print $2}')
sudo tee /etc/apt/sources.list.d/ddebs.list << EOF
deb http://ddebs.ubuntu.com/ ${codename}      main restricted universe multiverse
deb http://ddebs.ubuntu.com/ ${codename}-security main restricted universe multiverse
deb http://ddebs.ubuntu.com/ ${codename}-updates  main restricted universe multiverse
deb http://ddebs.ubuntu.com/ ${codename}-proposed main restricted universe multiverse
EOF
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ECDCAD72428D7C01
sudo apt-get update
sudo apt-get install -y linux-image-$(uname -r)-dbgsym
