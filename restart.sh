#!/bin/bash

function rhelp {
	echo "Restart"
	echo "-h  -- Prints this message and then exits."
	echo "-t [val] -- The amount of time to wait before starting pingMonitor.py."
	echo "    If this is left blank, then 5s is used."
}

if [ $# -eq 0 ]
then
	stime=5s
elif [ $1 -eq "-h" ]
then
	rhelp
	exit 0
elif [ $1 -eq "-t" ]
then
	stime=$2
fi

./stop.sh

sleep $stime

python pingMonitor.py

