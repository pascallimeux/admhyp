import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
from app.common.ssh import Ssh
from app.common.rcmds import create_remote_connection, check_ssh_admin_connection

class SshTest(unittest.TestCase):

    def test_create_remote_admin(self):
        hostname = "192.168.0.101"
        adminusername= "orangeadm"
        username="pascal"
        password="pascal"
        key_file = "/home/pascal/.ssh/id_rsa"
        pub_key_file="/home/pascal/.ssh/id_rsa.pub"
        create_remote_connection(hostname=hostname, password=password)
        with self.assertRaises(Exception) as context:
            print ("ERROR....{}".format(context.exception))

        check_ssh_admin_connection(hostname=hostname, remoteadminlogin=adminusername, key_file=key_file)
        try:
            ssh = Ssh(hostname=hostname, username=adminusername, key_file=key_file)
            ssh.exec_cmd("ls -lisa", sudo=True)
        finally:
            if ssh:
                ssh.close_connection()


if __name__ == '__main__':
    unittest.main()