class Node:
    def __init__(self, x, y, vel_x, vel_y, final_state, out):
        self.pos = (x, y)
        self.vel = (vel_x, vel_y)
        self.final_state = final_state
        self.out = out

    def __str__(self):
        return "node: pos=" + str(self.pos) + " velocity=" + str(self.vel) + " finalState?=" + str(self.final_state) + " out=" + str(self.out)

    def __repr__(self):
        return "node: pos=" + str(self.pos) + " velocity=" + str(self.vel) + " finalState?=" + str(self.final_state) + " out=" + str(self.out)

    def get_pos(self):
        return self.pos

    def get_pos_x(self):
        return self.pos[0]

    def get_pos_y(self):
        return self.pos[1]

    def get_vel(self):
        return self.vel

    def get_vel_x(self):
        return self.vel[0]

    def get_vel_y(self):
        return self.vel[1]

    def get_out(self):
        return self.out

    def get_final_state(self):
        return self.final_state

    def set_pos(self, x, y):
        self.pos = (x,y)

    def set_pos_x(self, x):
        self.pos[0] = x

    def set_pos_y(self, y):
        self.pos[y] = y

    def set_vel(self, vel_x, vel_y):
        self.vel = (vel_x, vel_y)

    def set_vel_x(self, vel_x):
        self.vel[0] = vel_x

    def set_vel_y(self, vel_y):
        self.vel[1] = vel_y

    def set_out(self, out):
        self.out = out

    def set_final_state(self, state):
        self.final_state = state

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel

    def __hash__(self):
        return hash((self.pos, self.vel))