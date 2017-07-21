# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

import os
from git import Repo, Git, remote
import logging
from subprocess import Popen, call, PIPE, STDOUT
from app.common.log import *
from app.common.log import get_logger
logger = get_logger()

# used to display download progress for git commands
class Progress(remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print ('update(%s, %s, %s, %s)'%(op_code, cur_count, max_count, message))

def SetupHyperledger():
    #CloneFabrics()
    CreateBinaries()
    CreateDockerImages()
    BuildTarBall()


def exec_local_cmd(cmd):
    #cmd = cmd.strip(" ")
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    for line in process.stdout:
        print (line.decode('utf-8'))
    process.wait()

def __buildHyperledgerRepo():
    if not os.path.exists(hyperledger_local_repo):
        logger.debug ("Create Hyperledger local repo: {0}".format(hyperledger_local_repo))
        exec_local_cmd("mkdir "+hyperledger_local_repo)

def CloneFabrics():
    __buildHyperledgerRepo()
    logger.debug("Clone fabric from gerrit with tag name={0}".format(tag_name))
    exec_local_cmd("rm -Rf "+fabric_local_repo)
    Repo.clone_from(git_url_fabric, fabric_local_repo, progress=Progress())
    g = Git(fabric_local_repo)
    g.checkout(tag_name)

    logger.debug("Clone fabric-ca from gerrit with tag name={0}".format(tag_name))
    exec_local_cmd("rm -Rf "+fabric_ca_local_repo)
    Repo.clone_from(git_url_fabric_ca, fabric_ca_local_repo, progress=Progress())
    g = Git(fabric_ca_local_repo)
    g.checkout(tag_name)

def __removeBinaries():
    logger.debug("Remove binaries...")
    cmd = "cd fabric_bin_local_repo && rm * >/dev/null 2>&1"
    exec_local_cmd("cd "+fabric_bin_local_repo+" ; rm * >/dev/null 2>&1")
    exec_local_cmd("cd "+fabric_ca_bin_local_repo+" ; rm * >/dev/null 2>&1")
    exec_local_cmd("cd "+binrepo+" ; rm * >/dev/null 2>&1")

def CreateBinaries():
    #__removeBinaries()
    logger.debug("Process building fabric-ca-server binary...")
    exec_local_cmd("cd " + fabric_ca_local_repo + " ; make fabric-ca-server")

    logger.debug("Process building fabric-ca-client binary...")
    exec_local_cmd("cd " + fabric_ca_local_repo + " ; make fabric-ca-client")

    logger.debug("Process building orderer binary...")
    exec_local_cmd("cd " + fabric_local_repo + " ; make orderer")

    logger.debug("Process building peer binary...")
    exec_local_cmd("cd " + fabric_local_repo + " ; make peer")

    logger.debug("Copy fabric binaries to {}".format(binrepo))
    exec_local_cmd("cp " + fabric_bin_local_repo +"/* " + binrepo)

    logger.debug("Copy fabric-ca binaries to {}".format(binrepo))
    exec_local_cmd("cp " + fabric_ca_bin_local_repo + "/* " + binrepo)


def CreateDockerImages():
    logger.debug("Process building zookeeper docker image...")
    exec_local_cmd("cd " + fabric_local_repo + " ; make zookeeper")

    logger.debug("Process building kafka docker image...")
    exec_local_cmd("cd " + fabric_local_repo + " ; make kafka")

    logger.debug("Save zookeeper image...")
    exec_local_cmd("docker save "+dockerimagerepo+"zookeeper.tar -o hyperledger/fabric-zookeeper")

    logger.debug("Save kafka image...")
    exec_local_cmd("docker save "+dockerimagerepo+"kafka.tar -o hyperledger/fabric-kafka")


def BuildTarBall(repo=binrepo, tarballname=tarballnamebinaries):
    logger.debug("Build tarball : tar cvzf {0}{1} {2}*".format(tarballsrepo, tarballname, repo))
    exec_local_cmd("cd "+repo +" ; tar cvzf " + tarballsrepo+tarballname+"*")
    #ExecSystemCmd("cd repo && tar cvzf " + tarballsrepo+"/"+tarballname+" *")

