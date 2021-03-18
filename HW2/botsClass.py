import struct

class Bot:

    def __init__(self, na, nb, nc):
        self.na = na
        self.nb = nb
        self.nc = nc
        self.first = True

    def play(self, data):
        if (self.first):
            data = struct.pack(">hhhhh", self.na, self.nb, self.nc, 4, 0)
            self.first = False
            return data, 1
        (H, v) = struct.unpack(">1ch", data)
        #H = H.decode()
        winner = 4
        notLegal = 1
        H = H.decode()
        if H == 'A':
            if v > self.na:
                notLegal = 2
            else:
                self.na -= v
        elif H == 'B':
            if v > self.nb:
                notLegal = 2
            else:
                self.nb -= v
        elif H == 'C':
            if v > self.nc:
                notLegal = 2
            else:
                self.nc -= v
        elif H == 'D':
            notLegal = 2
        else:
            dataz = struct.pack(">hhhhh", self.na, self.nb, self.nc, 3, 0)
            return dataz, 0

        if (self.na, self.nb, self.nc) == (0, 0, 0):
            winner = 2
            dataz = struct.pack(">hhhhh", self.na, self.nb, self.nc, winner, notLegal)
            return dataz, 0

        maxz = max(self.na, self.nb, self.nc)
        if maxz == self.na:
            self.na -= 1
        elif maxz == self.nb:
            self.nb -= 1
        elif maxz == self.nc:
            self.nc -= 1

        if (self.na, self.nb, self.nc) == (0, 0, 0):
            winner = 1
            dataz = struct.pack(">hhhhh", self.na, self.nb, self.nc, winner, notLegal)
            return dataz, 0

        dataz = struct.pack(">hhhhh", self.na, self.nb, self.nc, winner, notLegal)
        return dataz, 1
