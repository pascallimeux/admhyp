#!/usr/bin/env bash
PID=`pidof fabric-ca-server`
[ -n "$PID" ] && echo True || echo False