#!/usr/bin/env bash
cd ..
CMD="./fabric-ca-server start -b admin:'orange2017!' -c ./.msp/config.yaml > ./log/ca.log 2>&1 &"
eval "$CMD"