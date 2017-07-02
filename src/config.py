# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''


import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST='0.0.0.0'
PORT=4000
DEBUG = True

# logger file
LOGFILENAME = ROOT_DIR+"/log/admhyp.log"

# sqlite3 BDD file
SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/db/admhyp.db".format(ROOT_DIR)

# hyperledger tag version for github
HYP_TAG_NAME = "v1.0.0-beta"

# timeout for ssh connection
SSHCNXTIMEOUT = 3

# default port for ssh
SSHDEFAULTPORT = 22

# Credentials
USERADM = "orangeadm"
REMOTEUSERNAME = "pascal"
import getpass
LOCALLOGIN = getpass.getuser()
KEYFILE = os.getenv('HOME')+'/.ssh/id_rsa'
PUBKEYFILE = os.getenv('HOME')+'/.ssh/id_rsa.pub'

# application folders.
GOPATH  = "/opt/gopath"
BIN_DIR = ROOT_DIR+"/data/bin/"
CONF_DIR = ROOT_DIR+"/data/conf/"

MSREPO = " ../data/msp"
TGZREPO = "../data/tarballs/"
TGZBINNAME = "binaries.tgz"
DOCKERIMAGEREPO = "../data/dockerimage/"

fabric    = "fabric"
fabric_ca = "fabric-ca"
git_url_hyperledger = "https://gerrit.hyperledger.org/r/"
git_url_fabric = git_url_hyperledger + fabric+".git"
git_url_fabric_ca = git_url_hyperledger + fabric_ca+".git"

hyperledger_local_repo = os.environ.get("GOPATH") + "/src/github.com/hyperledger"
fabric_ca_local_repo = hyperledger_local_repo + "/" + fabric_ca
fabric_local_repo = hyperledger_local_repo + "/" + fabric
fabric_ca_bin_local_repo = fabric_ca_local_repo + "/bin"
fabric_bin_local_repo = fabric_local_repo + "/build/bin"





