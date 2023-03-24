#!/bin/bash

do_suspend() {
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
	sleep 1
	echo fix dual monitor black screen bug
	DISPLAY=:0.0 xset dpms force off; sleep 0.3; DISPLAY=:0.0 xset dpms force on
	sleep 3
	echo resync ntp datetime
	systemctl restart systemd-timesyncd.service
}

if [ "$1" == "once" ]; then
	echo once
	do_suspend
	exit 0
fi

#sleep infinity

monitor_state_timeout=0
monitor_state_timeout_limit=300
sleep_timeout=10

check_condition() {
	#DISPLAY=:0.0 xset q | grep "Monitor is Off"
	#monitor_state=$?
	#if [ $monitor_state -eq 0 ]; then
	#	monitor_state_timeout=$((monitor_state_timeout+sleep_timeout))
	#else
		monitor_state_timeout=0
	#fi
	#echo monitor_state_timeout $monitor_state_timeout

	# get lid state
	grep closed /proc/acpi/button/lid/LID*/state
	lid_state=$?
	if [ $lid_state -eq 0 ] || [ $monitor_state_timeout -ge $monitor_state_timeout_limit ] ; then
		return 0
	fi
	return 1
}

#add DISPLAY=:0.0 xhost SI:localuser:root to autorun
while true; do
	sleep $sleep_timeout;
	check_condition
	if [ $? -eq 0 ]; then
		sleep 5;
		check_condition
		if [ $? -eq 0 ]; then
			do_suspend
		fi
	else
		echo nosuspend
	fi
done
