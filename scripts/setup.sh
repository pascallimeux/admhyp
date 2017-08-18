#!/bin/bash
#
# Copyright Orange Labs Services. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m';
NC='\033[0m' # No Color
ACCOUNT=orange
ENC_PWD=C/b.O5rZyECPo  #to generate encryped password: openssl passwd 'PASSWORD'

function get_distribution {
    distribution="Unknown"
    while read -r line
    do
        element=$(echo $line | cut -f1 -d=)
        if [ "$element" = "ID" ]; then
            distribution=$(echo $line | cut -f2 -d=)
        fi
    done < "/etc/os-release"
    echo "${distribution//\"}"
}
DISTRIB=$(get_distribution)

function update_system(){
    sudo apt -y --fix-broken install > /dev/null 2>&1
    sudo apt update && sudo apt-upgrade > /dev/null 2>&1
    sudo apt install -y curl make git openssh-server
    sudo apt install -y build-essential python-dev gcc
	sudo apt install -y libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev
    echo -e "${GREEN}System is up to date!${NC}"
}

function create_admin_account(){
    if id "$1" >/dev/null 2>&1; then
        echo -e "${YELLOW}user $1 already exists!${NC}"
    else
        sudo useradd $1 -p $2 -m -U -s /bin/bash
        echo "$1 ALL=(ALL:ALL) NOPASSWD:ALL" > /tmp/$1
        sudo chown root.root /tmp/$1
        sudo chmod ug-w /tmp/$1
        sudo mv /tmp/$1 /etc/sudoers.d/$1
        if id "$1" >/dev/null 2>&1 && [ -f /etc/sudoers.d/$1 ]; then
            echo -e "${GREEN}user $1 created with sudo privileges${NC}"
        else
            echo -e "${RED}user $1 not created!${NC}"
        fi
    fi
}

function install_go(){
    curl -L https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz > /tmp/go1.8.linux-amd64.tar.gz
    tar -xvf /tmp/go1.8.linux-amd64.tar.gz >/dev/null 2>&1
    if [ -d /usr/local/go ]; then
        sudo rm -Rf /usr/local/go;
    fi
    sudo mv go /usr/local
    if [ -d "/opt/gopath" ]; then
        sudo mkdir -p /opt/gopath;
    fi
    sudo echo "export GOROOT=/usr/local/go" >> /tmp/go_profile
    sudo echo "export PATH=$PATH:/usr/local/go/bin" >> /tmp/go_profile
    sudo echo "export GOPATH=/opt/gopath" >> /tmp/go_profile
    sudo chown root.root /tmp/go_profile
    sudo chmod ug-w /tmp/go_profile
    sudo mv /tmp/go_profile /etc/profile.d/go_profile
    source /etc/profile.d/go_profile
    sudo echo "Installing dependencies..."
    go get -u github.com/axw/gocov/...
    go get -u github.com/AlekSi/gocov-xml
    go get -u github.com/client9/misspell/cmd/misspell
    go get -u github.com/golang/lint/golint
    go get -u golang.org/x/tools/cmd/goimports
    echo -e "${GREEN}$(go version) installed${NC}"
}

function install_docker(){
    case $DISTRIB in
            ubuntu)
                sudo apt -y install -y linux-image-extra-$(uname -r) linux-image-extra-virtual
                sudo apt -y install apt-transport-https ca-certificates
                sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
                sudo apt update
                sudo apt -y install docker.io docker-compose
                sudo apt -y install docker-engine
                sudo usermod -a -G docker $ACCOUNT
                sudo service docker start
                ;;
            debian)
                sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
                curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
                sudo apt-key fingerprint 0EBFCD88
                sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
                sudo apt-get update
                sudo apt-get install -y --allow-unauthenticated docker-ce
                sudo usermod -a -G docker $ACCOUNT
                sudo service docker start
                ;;
            *)
                echo -e "${RED}Linux distribution not compatible!!${NC}"
            return
            ;;
    esac
    echo "DOCKER_OPTS=\"-H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock \"" >  /etc/default/docker
    curl -L https://github.com/docker/compose/releases/download/1.13.0/docker-compose-`uname -s`-`uname -m` > /tmp/docker-compose
    sudo mv /tmp/docker-compose /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}$(docker --version) installed${NC}"
    echo -e "${GREEN}$(docker-compose --version) installed${NC}"
}

function install_python() {
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt update && sudo apt install -y python3.6
}

function install_mosquitto() {
    sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
    sudo apt update && sudo apt install mosquitto -y
    sudo apt install mosquitto-clients -y
    sudo service mosquitto restart
}

function generate_keys(){
    ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''
    chmod 600 $HOME/.ssh/id_rsa
}
#echo -e "${GREEN}distribution: $DISTRIB ${NC}"
#echo "${YELLOW}System updating.... ${NC}"
#update_system
#read -p "Press any key to create admin account: "
#create_admin_account $ACCOUNT $ENC_PWD
#read -p "Press any key to install go: "
install_go
install_python
install_mosquitto
generate_keys
#read -p "Press any key to install docker and docker-compose: "
#install_docker
