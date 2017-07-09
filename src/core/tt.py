
from subprocess import Popen, call, PIPE, STDOUT
import os, sys
import argparse
import  os, string

def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print (socket.gethostbyname(socket.gethostname()))
    local_ip=s.connect(('google.com', 0))
    return local_ip

def check_process():
    program = raw_input("Enter the name of the program to check: ")
    try:
        #perform a ps command and assign results to a list
        output = commands.getoutput("ps -ef |grep " + program)
        proginfo = string.split(output)
        #display results
        print (proginfo)
        print ("Full path:{0}  Owner:{1} 0  Process ID:{2}  Parent process ID:{3}  Time started:{4}".format(proginfo[5], proginfo[0], proginfo[1], proginfo[2],proginfo[4]))
    except:
        print ("There was a problem with the program.")

def getLocalIp():
    import os
    f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    ip=f.read()
    return ip

class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = '123456789'
    DEBUG = False
    TESTING = False
    HOST='0.0.0.0'
    PORT=4000
    KEYFILE = os.getenv('HOME') + '/.ssh/id_rsa'
    PUBKEYFILE = os.getenv('HOME') + '/.ssh/id_rsa.pub'
    USERADM = "orangeadm"
    REMOTEUSERNAME = "pascal"
    # sqlite3 BDD file
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/db/admhyp.db".format(ROOT_DIR)

    SSHCNXTIMEOUT = 3

    # default port for ssh
    SSHDEFAULTPORT = 22

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='Scaffold a Flask Skeleton.')
    parser.add_argument('appname', help='The application name')
    parser.add_argument('-s', '--skeleton', help='The skeleton folder to use.')
    parser.add_argument('-b', '--bower', help='Install dependencies via bower')
    parser.add_argument('-v', '--virtualenv', action='store_true')
    parser.add_argument('-g', '--git', action='store_true')
    args = parser.parse_args()
    return args



def test_process(cmd):
    cmd = cmd.strip(" ")
    output, error = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    if error:
        print (error.decode('utf-8'))
    return output, error

def exec_system_cmd(cmd):
    cmd = cmd.strip(" ")
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

    for line in process.stdout:
        print ("OUT: {}".format(line.decode('utf-8')))
    process.wait()
    return process.stdout, process.error

def mem():
    cwd = os.getcwd()
    cmd = "ls"
    fullpath = os.path.join(cwd, "tt")
    cmd = "ls"
    args = "-lisa"
    cmd = cmd + " " + args + " " + fullpath
    print (cmd)
    out, err = test_process("ls -lisa")
    print ("OUT: {}".format(out))
    print ("ERR: {}".format(err))

def get_external_ipaddress():
    import urllib.request
    extipaddr = urllib.request.urlopen('http://ident.me').read().decode('utf8')
    return extipaddr

def get_local_ipaddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipaddr=s.getsockname()[0]
    return (ipaddr)

if __name__ == "__main__":
    pass

