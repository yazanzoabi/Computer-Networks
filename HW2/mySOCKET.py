#!/usr/bin/python3
from socket import *
import sys
import errno


def createSoc():
    try:
        return socket(AF_INET, SOCK_STREAM)
    except OSError as e:
        print("Error Creating your Socket")
        print(e.strerror)
        sys.exit(1)
    
def bindSoc(soc, host, port):
    try:
        soc.bind((host, port))
    except OSError as e:
        print("Error binding socket")
        print(e.strerror)
        sys.exit(1)

def listenSoc(soc, backlog):
    try:
        soc.listen(backlog)
    except OSError as e:
        print("Error listening")
        print(e.strerror)
        sys.exit(1)

def acceptSoc(soc):
    try:
        (conn_sock, address) = soc.accept()
        return conn_sock, address
    except OSError as e:
        print("Error accepting")
        print(e.strerror)
        sys.exit(1)
    except KeyboardInterrupt:
            soc.close()
            sys.exit(1)

def connectSoc(soc, host, port):
    try:
        soc.connect((host, port))
    except OSError as e:
        if e.errno == errno.ECONNREFUSED:
            print("Connection refused from server")
            sys.exit(1)
        else:
            print(e.strerror)
            sys.exit(1)

def sendSoc(soc, data):
    try:
        return soc.send(data)
    except OSError as e:
        print("error sending")
        sys.exit(1)
        
    

def recSoc(soc,recSize):
    try:
        return soc.recv(recSize)
    except OSError as e:
        return b''
    except KeyboardInterrupt:
        return b''

def closeSoc(soc):
    try:
        soc.close()
    except OSError as e:
        print("Error while closing socket")
        print(e.strerror)
        sys.exit(1)
    except KeyboardInterrupt:
        soc.close()
        sys.exit(1)
