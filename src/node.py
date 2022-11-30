class Node:
    def __init__(self, pos, vel, crashed):
        self.pos = pos
        self.vel = vel
        self.crashed = crashed

    def __str__(self):
        return "pos=" + str(self.pos) + " velocity=" + str(self.vel) + " " + str(self.crashed)

    def __repr__(self):
        return "pos=" + str(self.pos) + " velocity=" + str(self.vel) + " " + str(self.crashed)

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel and self.crashed == other.crashed

    def __hash__(self):
        return hash((self.pos, self.vel))
