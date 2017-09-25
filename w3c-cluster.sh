#!/bin/sh
#
# Copyright (C) 2017, Jaguar Land Rover and/or collaborators.
#
# Licensed according to the terms provided by the LICENSE file.
#
# Run the W3C demo insturment cluster with
# Crossbar as W3C VIS Server.
#

# Variables
WD=`pwd`
VSI_FILE="genivi-demo.vsi"
VSSI_EXEC=$WD/vsi/importVSS
CROSSBAR_EXEC=/usr/bin/crossbar
CAND_EXEC=$WD/vsi/vsi-socketcand
CAND_DEV="can0"
CAND_PID="$CAND_EXEC.pid"

#LOG_FILE="cluster.log"
#LOG_FILE="/dev/null"
LOG_FILE="/dev/stdout"

# Setup environment
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$WD/vsi:.
export PYTHONPATH=${PYTHONPATH}:$WD/vsi


start() {
    echo -n "Starting GENIVI W3C Demo Cluster... "
    rm /var/run/shm/vsi* >$LOG_FILE 2>$LOG_FILE
    $VSSI_EXEC $VSI_FILE >>$LOG_FILE 2>>$LOG_FILE
    $CAND_EXEC -p $CAND_PID $VSI_FILE $CAND_DEV
    $CROSSBAR_EXEC start >>$LOG_FILE 2>>$LOG_FILE &
    echo "running"
}

stop() {
    echo -n "Stopping GENIVI W3C Demo Cluster... "
    $CROSSBAR_EXEC stop >>$LOG_FILE 2>>$LOG_FILE
    kill -9 $(<"$CAND_PID")
    rm /var/run/shm/vsi* >>$LOG_FILE 2>>$LOG_FILE
    echo "stopped"
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
        echo "Usage: "$0" {start|stop|restart}"
        exit 1
        ;;
esac

exit 0
