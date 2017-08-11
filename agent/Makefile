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
# clean: stops docker conatainers used for integration testing
#

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
	@go get github.com/eclipse/paho.mqtt.golang
	@go get golang.org/x/net/websocket
	@go get golang.org/x/net/proxy
	@go get github.com/op/go-logging

