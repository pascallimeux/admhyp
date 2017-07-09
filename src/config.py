# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''


import os, sys, logging
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def appconf():
    args = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig').split(".")
    module = args[0]
    classname = args[1]
    return getattr(__import__(module), classname)

import getpass
LOCALLOGIN = getpass.getuser()




# hyperledger tag version for github
HYP_TAG_NAME = "v1.0.0-beta"

# application folders.
GOPATH = "/opt/gopath"
BIN_DIR = ROOT_DIR + "/data/bin/"
CONF_DIR = ROOT_DIR + "/data/conf/"

MSREPO = " ../data/msp"
TGZREPO = "../data/tarballs/"
TGZBINNAME = "binaries.tgz"
DOCKERIMAGEREPO = "../data/dockerimage/"

fabric = "fabric"
fabric_ca = "fabric-ca"
git_url_hyperledger = "https://gerrit.hyperledger.org/r/"
git_url_fabric = git_url_hyperledger + fabric + ".git"
git_url_fabric_ca = git_url_hyperledger + fabric_ca + ".git"

hyperledger_local_repo = os.environ.get("GOPATH") + "/src/github.com/hyperledger"
fabric_ca_local_repo = hyperledger_local_repo + "/" + fabric_ca
fabric_local_repo = hyperledger_local_repo + "/" + fabric
fabric_ca_bin_local_repo = fabric_ca_local_repo + "/bin"
fabric_bin_local_repo = fabric_local_repo + "/build/bin"

class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = '123456789'
    DEBUG = False
    TESTING = False
    HOST=None
    PORT=4000
    KEYFILE = os.getenv('HOME') + '/.ssh/id_rsa'
    PUBKEYFILE = os.getenv('HOME') + '/.ssh/id_rsa.pub'
    USERADM = "orangeadm"
    REMOTEUSERNAME = "pascal"
    # sqlite3 BDD file
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/db/admhyp.db".format(ROOT_DIR)

    #  timeout for ssh connection
    SSHCNXTIMEOUT = 3

    # default port for ssh
    SSHDEFAULTPORT = 22

    # default log level
    LOG_LEVEL = logging.INFO

    # logger file
    LOGFILENAME = ROOT_DIR + "/log/admhyp.log"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    APPMODE = "dev"
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class TestingConfig(BaseConfig):
    """Testing configuration."""
    APPMODE = "test"
    DEBUG = True
    TESTING = True

class ProductionConfig(BaseConfig):
    """Production configuration."""
    APPMODE = "prod"
    SECRET_KEY = os.urandom(12)
    DEBUG = False