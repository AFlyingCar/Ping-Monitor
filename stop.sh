#!/bin/bash

echo "Terminating Ping Monitor..."

if [ -f ./.pmlock ]
then
	# Need Administrator permission before quitting Ping Monitor
	echo "Ready to delete .pmlock"
	sudo rm -f ./.pmlock
fi

