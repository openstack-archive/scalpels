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
# TODO enable mysql log
mysql -e "SET GLOBAL $log_switch_var= 'ON';"

# TODO tail the logfile
old_log_file=`mysql -e "SELECT @@$log_file_var" | grep -v general_log_file | grep -v '\-\-\-\-\-'`
mysql -e "SET GLOBAL $log_file_var= '$log_file';"


# TODO reset everything back
mysql -e "SET GLOBAL $log_switch_var= 'OFF';"
mysql -e "SET GLOBAL $log_file_var= '$old_log_file';"
