# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''


from subprocess import Popen, PIPE, STDOUT, CalledProcessError

def exec_local_cmd(cmd):
    try:
        #cmd = cmd.strip(" ")
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in process.stdout:
            print (line.decode('utf-8'))
        process.wait()
    except Exception as e:
        print (e)

def exec_cmd(cmd):
    try:
        pipe = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        lines =""
        while pipe.poll() is None:
            lines = lines + pipe.stdout.readline().decode('utf-8')
        return lines, None
    except CalledProcessError as error:
        return lines, str(error.output)

if __name__ == "__main__":
    cmd = "who && ss -na |grep 127.0.0.1 |grep tcp"
    cmd2 = "kill -9 2425"
    response, error = exec_cmd(cmd2)
    print ("response: {0} \nerror: {1}".format(response, error ))