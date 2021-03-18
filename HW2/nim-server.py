#!/usr/bin/python3
import sys
import socket
from trafficHandler import trafficHandler
from botsClass import Bot

def clearLists(games, connections):
    res = list(filter(None, games))
    games = res
    res = list(filter(None, connections))
    connections = res
    return games, connections


def main():
    NA = int(sys.argv[1])
    NB = int(sys.argv[2])
    NC = int(sys.argv[3])
    numPlayers = int(sys.argv[4])
    waitListSize = int(sys.argv[5])
    if len(sys.argv) == 7:
        PORT = int(sys.argv[6])
    else:
        PORT = 6444
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', PORT))
    server_socket.listen(5)

    games = []                         ##size <= num-players
    connections = []                    ##size <= num-players
    trafficOUT = [None] * numPlayers
    Queue = []
    TH = trafficHandler(numPlayers, waitListSize)

    while True:
        while True:
            connections = [server_socket] + connections
            try:
                newConnections, trafficIN = TH.readFromClients(connections, server_socket)
                connections = connections[1:]
            except KeyboardInterrupt:
                server_socket.close()
                sys.exit(1)

            for i in range(len(connections)):
                if trafficIN[i] == "closed":
                    connections[i] = None
                    games[i] = None
            games, connections = clearLists(games, connections)

            Queue = Queue + newConnections
            for i in range(len(Queue)):
                if len(connections) < numPlayers:
                    connections.append(Queue[i])
                    games.append(Bot(NA, NB, NC))
                    trafficOUT[len(connections)+i-1] = games[-1].play(None)[0]
                    Queue[i] = None

            res = list(filter(None, Queue))
            Queue = res

            for i in range(len(connections)):
                if trafficIN[i] is not None and trafficIN[i] != "closed":
                    answer, gameStatus = games[i].play(trafficIN[i])
                    trafficOUT[i] = answer
                    if gameStatus == 0:
                        games[i] = None

            Rejected = Queue[waitListSize:]
            Queue = Queue[:waitListSize]
            TH.sendToRejected(Rejected)
            TH.sendToQueue(Queue)

            TH.writeToClients(connections, trafficOUT)
            trafficOUT = [None] * numPlayers

            for i in range(len(connections)):
                if games[i] is None:
                    connections[i] = None
            games, connections = clearLists(games, connections)

if __name__ == "__main__":
    main()

