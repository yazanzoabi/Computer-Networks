#!/usr/bin/python3
import sys
import struct
from MySocketClass import MySocket


def main():
    if len(sys.argv) != 1:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
    else:
        HOST = 'localhost'
        PORT = 6444

    clientSock = MySocket(sendSize=3, recSize=10)
    clientSock.myConnect(HOST, PORT)

    gameStatus = 4
    while gameStatus:
        dataz = clientSock.myRecv()
        if dataz == 0:
            print("Disconnected from server")
            clientSock.myClose()
            sys.exit(1)
        (n1, n2, n3, gameStatus, isLegal) = struct.unpack(">hhhhh", dataz)
        if isLegal == 1:
            print("Move accepted")
        elif isLegal == 2:
            print("Illegal move")
        if gameStatus == 3:
            clientSock.myClose()
            sys.exit(0)
        print("Heap A: " + str(n1))
        print("Heap B: " + str(n2))
        print("Heap C: " + str(n3))
        if gameStatus == 1:
            print("Server win!")
            clientSock.myClose()
            sys.exit(0)
        if gameStatus == 2:
            print("You win!")
            clientSock.myClose()
            sys.exit(0)

        print("Your turn:")
        controlz = input()
        dataz = isLegalMove(controlz)
        clientSock.mySend(dataz)

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
