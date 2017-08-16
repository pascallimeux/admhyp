#
# Copyright OrangeLabs Inc. All Rights Reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# This MakeFile assumes that fabric, and fabric-ca were cloned and their docker
# images were created using the make docker command in the respective directories
#
# Supported Targets:
# all : runs unit and integration tests
# depend: installs test dependencies
# unit-test: runs all the unit tests
# integration-test: runs all the integration tests
# clean: stops docker containers used for integration testing
#

PUBKEY="$(shell cat /home/pascal/.ssh/id_rsa.pub)"

.DEFAULT_GOAL := bin
.PHONY: help
help:
	@echo
	@echo
	@echo ' -------'
	@echo '  Agent '
	@echo ' -------'
	@echo
	@echo 'Usage:'
	@echo ' make init-env        Init Go environnement.'
	@echo
	@echo

init-env:
	@sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
	@sudo apt update && sudo apt install mosquitto -y
	@sudo apt install mosquitto-clients -y
	@sudo service mosquitto restart
	@sudo apt install upx -y
	@go get github.com/eclipse/paho.mqtt.golang
	@go get golang.org/x/net/websocket
	@go get golang.org/x/net/proxy
	@go get github.com/op/go-logging
	@go get github.com/shirou/gopsutil/...

build:
	@GOOS=linux go build -ldflags="-s -w" -o ./bin/hyp-agent agent.go

build-prod:
	@GOOS=linux go build -ldflags="-s -w" -o ./bin/hyp-agent agent.go
	@upx -9 ./bin/hyp-agent

run:
	@sudo ./bin/hyp-agent -broker="tcp://localhost:1883" -pubkey=${PUBKEY} -loglevel=debug -init=false -name=agent1

stop:
	@sudo pkill -f hyp-agent

clean:
	@sudo rm /etc/sudoers.d/orangeadm
	@sudo rm -R /var/hyperledger
	@sudo userdel -r orangeadm
	@sudo rm -R /lib/systemd/system/hyp-agent.service
	@sudo systemctl stop hyp-agent.service
	@sudo systemctl disable hyp-agent.service