#!/usr/bin/python3
import sys
import struct
from MySocketClass import MySocket


def main():
    MySocket.MSG_SENT_SIZE = 10
    MySocket.MSG_REC_SIZE = 3
    NA = int(sys.argv[1])
    NB = int(sys.argv[2])
    NC = int(sys.argv[3])
    if len(sys.argv) == 5:
        PORT = int(sys.argv[4])
    else:
        PORT = 6444

    serverSock = MySocket(sendSize=10, recSize=3)
    serverSock.myBind('', PORT)
    serverSock.myListen(5)

    while True:
        (conn_sock, address) = serverSock.myAccept()
        na = NA
        nb = NB
        nc = NC
        winner = 4
        data = struct.pack(">hhhhh", na, nb, nc, 4, 0)
        conn_sock.mySend(data)
        while True:
            notLegal = 1
            data = conn_sock.myRecv()
            if data == 0:
                conn_sock.myClose()
                break

            (H, v) = struct.unpack(">1ch", data)
            H = H.decode()
            if H == 'A':
                if v > na :
                    notLegal = 2
                else:
                    na -= v
            elif H == 'B':
                if v > nb:
                    notLegal = 2
                else:
                    nb -= v
            elif H == 'C':
                if v > nc:
                    notLegal = 2
                else:
                    nc -= v
            elif H == 'D':
                notLegal = 2
            else:
                dataz = struct.pack(">hhhhh", na, nb, nc, 3, 0)
                conn_sock.mySend(dataz)
                conn_sock.myClose()
                break

            if (na, nb , nc) == (0,0,0):
                winner = 2
                dataz = struct.pack(">hhhhh", na, nb, nc, winner, notLegal)
                conn_sock.mySend(dataz)
                conn_sock.myClose()
                break

            maxz = max(na, nb, nc)
            if maxz == na:
                na -= 1
            elif maxz == nb:
                nb -= 1
            elif maxz == nc:
                nc -= 1

            if (na, nb, nc) == (0,0,0):
                winner = 1
                dataz = struct.pack(">hhhhh", na, nb, nc, winner, notLegal)
                conn_sock.mySend(dataz)
                conn_sock.myClose()
                break

            dataz = struct.pack(">hhhhh", na, nb, nc, winner, notLegal)
            conn_sock.mySend(dataz)

if __name__ == "__main__":
    main()