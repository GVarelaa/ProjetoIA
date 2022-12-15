class Node:
    def __init__(self, pos, vel, crashed):
        self.pos = pos
        self.vel = vel
        self.crashed = crashed

    def __str__(self):
        return "Position =" + str(self.pos) + " | Velocity=" + str(self.vel) + " | Is_Crashed : " + str(self.crashed)

    def __repr__(self):
        return "Position =" + str(self.pos) + "| Velocity=" + str(self.vel) + " | Is_Crashed : " + str(self.crashed)

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel

    def __hash__(self):
        return hash((self.pos, self.vel))
