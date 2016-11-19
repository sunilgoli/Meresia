#!/bin/sh

projectdir="/Users/sunilgoli/Documents/workspace/python/meresia/server"

start() {
	cd $projectdir
	python start.py
	echo "Server started"
}

stop() {
	echo "Processes running:"
	ps -ef | grep 'start.py' | awk '{ print $2 }'
	for pid in $(ps -ef | grep 'start.py' | awk '{ print $2 }'); do kill -9 $pid; done
	sleep 2
	echo "Server stopped"
}

case "$1" in
		start)
			start
		;;
		stop)
			stop
		;;
		restart)
			stop
			start
		;;
	*)
	echo "Usage: ./server_startstop.sh start | ./server_startstop.sh stop | ./server_startstop.sh restart"
    exit 1
esac
exit 0
