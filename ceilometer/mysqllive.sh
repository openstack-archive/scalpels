#!/bin/bash
# Author: Kun Huang <academicgareth@gmail.com>
#
# Basic Usage: TODO
#
# TODO announce the advantage and disadvantages
#

log_file_var=general_log_file
log_switch_var=general_log
# TODO enable mysql log
mysql -e "SET GLOBAL $log_switch_var= 'ON';"

# TODO tail the logfile
logfile=`mysql -e "SELECT @@$log_file_var" | grep -v general_log_file | grep -v '\-\-\-\-\-'`
tailf $logfile

# TODO disable mysql log
mysql -e "SET GLOBAL $log_switch_var= 'OFF';"
