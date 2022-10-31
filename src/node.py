class Node:
    def __init__(self, x, y, vel_x, vel_y, is_final_state, is_out):
        self.pos = (x, y)
        self.vel = (vel_x, vel_y)
        self.is_final_state = is_final_state
        self.is_out = is_out

    def __str__(self):
        return "node: pos=" + str(self.pos) + " velocity=" + str(self.vel) + " is_final_state=" + str(self.is_final_state) + " is_out=" + str(self.is_out)

    def __repr__(self):
        return "node: pos=" + str(self.pos) + " velocity=" + str(self.vel) + " is_final_state=" + str(self.is_final_state) + " is_out=" + str(self.is_out)

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

    def get_is_final_state(self):
        return self.is_final_state

    def get_is_out(self):
        return self.is_out

    def set_pos(self, x, y):
        self.pos = (x, y)

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

    def set_is_final_state(self, is_final_state):
        self.is_final_state = is_final_state

    def set_is_out(self, is_out):
        self.is_out = is_out

    def __eq__(self, other):
        return self.pos == other.pos and self.vel == other.vel

    def __hash__(self):
        return hash((self.pos, self.vel))