#!/usr/bin/env bash
PID=`pidof fabric-ca-server`
if [ -n $PID ]
then
    kill -9 $PID 2>/dev/null
else
    echo "peer does not work!"
fi