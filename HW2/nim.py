#!/usr/bin/python3
import sys
import struct
from select import *
import mySOCKET as mysoc


def main():
    first = True
    playing = False
    if len(sys.argv) != 1:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
    else:
        HOST = 'localhost'
        PORT = 6444

    clientSock = mysoc.createSoc()
    mysoc.connectSoc(clientSock, HOST, PORT)


    ##clientSock = MySocket(sendSize=3, recSize=10)

    gameStatus = 4
    serverPlayed = False
    recvd = 0
    blocks = []
    totalsent = 0
    while gameStatus:
        controlz = None

        r, w, x = select([sys.stdin, clientSock], [], [], 1)
        if r == []:
            continue
        for s in r:
            if s is clientSock:  ## if client sock is ready for reading
                block = mysoc.recSoc(clientSock,10-recvd)
                recvd += len(block)
                if block == b'':
                    dataz = 0
                else:
                    blocks.append(block)
                    if recvd >= 10:
                        dataz = b''.join(blocks)
                        blocks = []
                        recvd = 0
                    else:
                        break



                if dataz == 0:
                    print("Disconnected from server")
                    mysoc.closeSoc(clientSock)
                    sys.exit(1)

                (n1, n2, n3, gameStatus, isLegal) = struct.unpack(">hhhhh", dataz)
                if gameStatus == 5:
                    if first:
                        first = False
                        print("Waiting to play against the server.")
                    continue
                if gameStatus == 6:
                    print("You are rejected by the server.")
                    sys.exit(1)
                if playing == False:
                    print("Now you are playing against the server!")
                    playing = True
                if isLegal == 1:
                    print("Move accepted")
                elif isLegal == 2:
                    print("Illegal move")
                if gameStatus == 3:
                    mysoc.closeSoc(clientSock)
                    sys.exit(0)
                print("Heap A: " + str(n1))
                print("Heap B: " + str(n2))
                print("Heap C: " + str(n3))
                if gameStatus == 1:
                    print("Server win!")
                    mysoc.closeSoc(clientSock)
                    sys.exit(0)
                if gameStatus == 2:
                    print("You win!")
                    mysoc.closeSoc(clientSock)
                    sys.exit(0)

                print("Your turn:")
                serverPlayed = True

            else:  ## if there is ready input
                if controlz == None:
                    controlz = input()
                if controlz == "Q":
                    mysoc.closeSoc(clientSock)
                    sys.exit(1)
                if serverPlayed:
                    r1,w1,x1 = select([], [clientSock], [], 1)
                    dataz = isLegalMove(controlz)
                    sent = mysoc.sendSoc(clientSock,dataz[totalsent:])
                    
                    if sent == 0:
                        print("failed to send data")
                        sys.exit(1)
                    totalsent += sent
                    if totalsent >= 3:
                        totalsent = 0
                        dataz = b''
                    else:
                        break;


def isLegalMove(control):
    data = 0
    control = control.split(' ')
    if len(control) == 1:
        if control[0] == 'Q':
            return struct.pack(">ch", 'Z'.encode(), 0)
        else:
            data = struct.pack(">ch", 'D'.encode(), 0)
    elif len(control) == 2:
        heap = control[0]
        if heap != 'A' and heap != 'B' and heap != 'C':
            data = struct.pack(">ch", 'D'.encode(), 0)
        else:
            try:
                v = int(control[1])
                if 1000 > v > 0:
                    data = struct.pack(">ch", control[0].encode(), v)
                else:
                    data = struct.pack(">ch", 'D'.encode(), 0)
            except ValueError:
                data = struct.pack(">ch", 'D'.encode(), 0)
    else:
        data = struct.pack(">ch", 'D'.encode(), 0)

    return data


if __name__ == "__main__":
    main()
