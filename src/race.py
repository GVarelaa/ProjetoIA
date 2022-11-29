from node import Node
from parser import parser
from graph import Graph


class Race:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.graph = Graph()
        self.start = start
        self.end = end

    def __str__(self):
        return str(self.matrix) + str(self.graph)

    def next_state(self, state, accel_pair):
        # Given an initial state, returns a resulting state
        # According to the choices of accelerations (acX, acY)
        # And to the matrix (map) of the circuit

        # displacements
        disp_x = state.vel[0] + accel_pair[0]
        disp_y = state.vel[1] + accel_pair[1]

        curr_pos_x = state.pos[0]
        curr_pos_y = state.pos[1]

        curr_vel_x = state.vel[0]
        curr_vel_y = state.vel[1]

        # Values if there are no obstacles in the way
        new_pos_x = curr_pos_x + disp_x
        new_pos_y = curr_pos_y + disp_y
        new_vel_x = curr_vel_x + accel_pair[0]
        new_vel_y = curr_vel_y + accel_pair[1]
        crashed = False

        # Deslocamento horizontal
        for i in range(1, abs(disp_x) + 1):
            inc = -1
            mult = 1

            if disp_x < 0:
                mult = -1

            if self.matrix[curr_pos_x + i * mult][curr_pos_y] == 'F':
                return Node(curr_pos_x + i * mult, curr_pos_y, new_vel_x, new_vel_y, True, False, accel_pair)

            if self.matrix[curr_pos_x + i * mult][curr_pos_y] == 'X':
                crashed = True
                new_vel_x = new_vel_y = 0
                new_pos_x = curr_pos_x + i * mult + inc * mult

                break

        # Deslocamento vertical
        for j in range(1, abs(disp_y) + 1):
            inc = -1
            mult = 1

            if disp_y < 0:
                mult = -1

            if self.matrix[new_pos_x][curr_pos_y + j * mult] == 'F':
                return Node(curr_pos_x, curr_pos_y + j * mult, new_vel_x, new_vel_y, True, False, accel_pair)

            if self.matrix[new_pos_x][curr_pos_y + j * mult] == 'X':
                crashed = True
                new_vel_y = new_vel_x = 0
                new_pos_y = curr_pos_y + j * mult + inc * mult

                break

        new_state = Node(new_pos_x, new_pos_y, new_vel_x, new_vel_y, False, crashed, accel_pair)
        #print(new_state)
        return new_state

    def expand_state(self, state):
        nodes = list()

        nodes.append(self.next_state(state, (1, 1)))
        nodes.append(self.next_state(state, (1, -1)))
        nodes.append(self.next_state(state, (1, 0)))
        nodes.append(self.next_state(state, (-1, 1)))
        nodes.append(self.next_state(state, (-1, -1)))
        nodes.append(self.next_state(state, (0, -1)))
        nodes.append(self.next_state(state, (-1, 0)))
        nodes.append(self.next_state(state, (0, 0)))
        nodes.append(self.next_state(state, (0, 1)))

        return nodes

    def build_graph(self):
        states = []
        initial_node = Node()
        states.append(self.start)

        visited = []
        visited.append(self.start)

        while states != []:
            state = states.pop()
            expansion = self.expand_state(state)

            for e in expansion:
                if e.crashed:
                    self.graph.add_edge(state, e, 25)
                else:
                    self.graph.add_edge(state, e, 1)

                if e not in visited:
                    states.append(e)
                    visited.append(e)
