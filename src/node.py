class Node:
    def __init__(self, pos, vel, is_final_state, crashed, last_acc):
        self.pos = pos
        self.vel = vel
        self.is_final_state = is_final_state
        self.crashed = crashed
        #self.last_acc = last_acc

    def __str__(self):
        return "pos=" + str(self.pos) + " velocity=" + str(self.vel) + " " + str(self.is_final_state) + " " + str(self.crashed) + " " #+ str(self.last_acc)

    def __repr__(self):
        return "pos=" + str(self.pos) + " velocity=" + str(self.vel) + " " + str(self.is_final_state) + " " + str(self.crashed) + " " #+ str(self.last_acc)

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel and self.is_final_state == other.is_final_state \
                and self.crashed == other.crashed #and self.last_acc == other.last_acc

    def __hash__(self):
        return hash((self.pos, self.vel))