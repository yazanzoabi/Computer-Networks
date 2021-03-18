import select
import struct
import mySOCKET as mysoc
class trafficHandler:

    def __init__(self, numPlayers, waitListSize):
        self.numPlayers = numPlayers
        self.waitListSize = waitListSize
        self.readFromClientsDic = {}
        self.sendToClientsDic = {}
        self.sendToQueueDic = {}
        self.sendToRejectedDic = {}

    def _getIndex(self, fds,  connections):
        i = 0
        for fd in connections:
            if(fd == fds):
                return i
            else:
                i = i + 1
        return -1

    #this function read messages from client and scans for new connections on the server_socket
    def readFromClients(self, connections, server_socket):
        newConnections = []
        trafficIN = [None]*self.numPlayers
        infds, outfds, errfds = select.select(connections, [], [], 1)
        for fds in infds:
            if fds is server_socket:
                newClient, address = fds.accept()
                newConnections.append(newClient)
            else:
                i = self._getIndex(fds, connections)
                if i != -1:
                    if fds in self.readFromClientsDic:
                        blocks, totalsent = self.readFromClientsDic.get(fds)
                    else:
                        blocks = []
                        totalsent = 0
                    block = mysoc.recSoc(fds,1024)
                    totalsent += len(block)
                    if block == b'':
                        trafficIN[i-1] = "closed"
                    else:
                        blocks.append(block)
                        if totalsent >= 3:
                            trafficIN[i-1] = b''.join(blocks)
                            if fds in self.readFromClientsDic:
                                self.readFromClientsDic.pop(fds)
                        else:
                            self.readFromClientsDic.update({fds: (blocks, totalsent)})

        return newConnections, trafficIN



    #this functions sends the current game statuses to the client side
    def writeToClients(self, connections, trafficOUT):
        if connections == []:
            return
        infds, outfds, errfds = select.select([], connections, [], 0.1)
        for fds in outfds:
            i = self._getIndex(fds, connections)
            if trafficOUT[i] != None:
                if fds in self.sendToClientsDic:
                    totalsent = self.sendToClientsDic.get(fds)
                    sent = fds.send(trafficOUT[i][totalsent:])
                else:
                    totalsent = 0
                    sent = mysoc.sendSoc(fds,trafficOUT[i])
                totalsent += sent
                if totalsent < 10:
                    self.sendToClientsDic.update({fds: totalsent})
                elif fds in self.sendToClientsDic:
                    self.sendToClientsDic.pop(fds)

    #this function tells new clients that they are on the waiting list
    def sendToQueue(self, Queue):
        infds, outfds, errfds = select.select(Queue, [], [], 0.1)
        for s in infds:
            incoming = s.recv(1024)
            if incoming == b'':
                Queue.remove(s)
        
        if Queue == []:
            return
        waitinglistdata = struct.pack(">hhhhh", 0, 0, 0, 5, 0)
        infds, outfds, errfds = select.select([], Queue, [], 0.1)
        for socket in outfds:
            if socket in self.sendToQueueDic:
                totalsent = self.sendToQueueDic.get(socket)
            else:
                totalsent = 0
            sent = mysoc.sendSoc(socket,waitinglistdata)
            totalsent += sent
            if totalsent < 10:
                self.sendToQueueDic.update({socket: totalsent})
            elif socket in self.sendToQueueDic:
                self.sendToQueueDic.pop(socket)

    #this function tells Rejected clients that they are rejected
    def sendToRejected(self, Rejects):
        if Rejects == []:
            return
        Rejecteddata = struct.pack(">hhhhh", 0, 0, 0, 6, 0)
        infds, outfds, errfds = select.select([], Rejects, [], 0.1)
        i = 0
        for socket in outfds:
            if socket in self.sendToRejectedDic:
                totalsent = self.sendToRejectedDic.get(socket)
            else:
                totalsent = 0
            sent = mysoc.sendSoc(socket,Rejecteddata)##rejected
            totalsent += sent
            if totalsent < 10:
                self.sendToRejectedDic.update({socket: totalsent})
            else:
                Rejects[i] = None
                i = i + 1
                if socket in self.sendToRejectedDic:
                    self.sendToRejectedDic.pop(socket)

