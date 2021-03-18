#!/usr/bin/python3

import socket
import sys
import errno


class MySocket:

    def __init__(self, sendSize, recSize, sock=None):
        self.sendSize = sendSize
        self.recSize = recSize
        if sock is None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except OSError as e:
                print("Error Creating your Socket")
                print(e.strerror)
                sys.exit(1)
        else:
            self.sock = sock

    def myBind(self, host, port):
        try:
            self.sock.bind(('', port))
        except OSError as e:
            print("Error binding socket")
            print(e.strerror)
            sys.exit(1)

    def myListen(self, backlog):
        try:
            self.sock.listen(5)
        except OSError as e:
            print("Error listening")
            print(e.strerror)
            sys.exit(1)

    def myAccept(self):
        try:
            (conn_sock, address) = self.sock.accept()
            return MySocket(sendSize=10, recSize= 3, sock=conn_sock), address
        except OSError as e:
            print("Error accepting")
            print(e.strerror)
            sys.exit(1)
        except KeyboardInterrupt:
            self.sock.close()
            sys.exit()

    def myConnect(self, host, port):
        try:
            self.sock.connect((host, port))
        except OSError as e:
            if e.errno == errno.ECONNREFUSED:
                print("Connection Refused from server")
                sys.exit(1)
            else:
                print(e.strerror)
                sys.exit(1)

    def mySend(self, data):
        totalSent = 0
        while totalSent < self.sendSize:
            try:
                sent = self.sock.send(data[totalSent:])
                if sent == 0:
                    print("Failed to send data - connection broken (sent is 0)")
                    sys.exit(1)
            except OSError as e:
                print("Error sending data")
                print(e.strerror)
                sys.exit(1)
            totalSent = totalSent + sent

    def myRecv(self):
        blocks = []
        recvd = 0
        while recvd < self.recSize:
            try:
                block = self.sock.recv(self.recSize - recvd)
                if block == b'':
                    return 0
                blocks.append(block)
                recvd = recvd + len(block)
            except OSError as e:
                return 0
            except KeyboardInterrupt:
                self.sock.close()
                sys.exit(1)
        return b''.join(blocks)

    def myClose(self):
        try:
            self.sock.close()
        except OSError as e:
            print("Error while closing socket")
            print(e.strerror)
            sys.exit(1)
        except KeyboardInterrupt:
            self.sock.close()
            sys.exit(1)
