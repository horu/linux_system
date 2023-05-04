#!/bin/bash

echo sync
sync
#echo sleep 3
#sleep 3
#echo drop_caches
#echo 1 > /proc/sys/vm/drop_caches
#echo sleep 3
#sleep 3
#echo service bluetooth restart
#service bluetooth restart
##echo rm -f /var/log/pm-suspend.log
##rm -d /var/log/pm-suspend.log
##echo /sys/power/pm_trace
##echo 1 > /sys/power/pm_trace
#echo suspend
#systemctl suspend
##echo PM_DEBUG=true pm-suspend
##PM_DEBUG=true pm-suspend
echo mem > /sys/power/state
