#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>
#
# Basic Usage: TODO
#
# TODO announce the advantage and disadvantages
#

log_file_var=general_log_file
log_switch_var=general_log
log_file=/tmp/mysqllive.log
old_log_file=`mysql -e "SELECT @@$log_file_var" | grep -v $log_file_var | grep -v '\-\-\-\-\-'`
old_log_switch=`mysql -e "SELECT @@$log_switch_var" | grep -v $log_switch_var | grep -v '\-\-\-\-\-'`

# TODO enable mysql log
mysql -e "SET GLOBAL $log_file_var= '$log_file';"
mysql -e "SET GLOBAL $log_switch_var= 'ON';"

sudo tailf $log_file

# TODO reset everything back
mysql -e "SET GLOBAL $log_switch_var= '$old_log_switch';"
mysql -e "SET GLOBAL $log_file_var= '$old_log_file';"
sudo rm $log_file
