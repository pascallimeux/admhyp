# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''
import uuid, hashlib

def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

if __name__ == "__main__":
    password = 'pascal'
    hashed_password = hash_password(password)
    print (hashed_password)
    print (check_password(hashed_password, password))
