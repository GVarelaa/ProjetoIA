from node import Node
from parser import parser
from graph import Graph


class Race:
    def __init__(self, matrix, graph):
        self.matrix = matrix
        self.graph = graph

    def __str__(self):
        return str(self.matrix) + str(self.graph)

    def next_state(self, state, accel_pair):
        # Given an initial state, returns a resulting state
        # According to the choices of accelerations (acX, acY)
        # And to the matrix (map) of the circuit

        # displacements
        disp_x = state.get_vel_x() + accel_pair[0]
        disp_y = state.get_vel_y() + accel_pair[1]

        curr_pos_x = state.get_pos_x()
        curr_pos_y = state.get_pos_y()

        curr_vel_x = state.get_vel_x()
        curr_vel_y = state.get_vel_y()

        # Values if there are no obstacles in the way
        new_pos_x = curr_pos_x + disp_x
        new_pos_y = curr_pos_y + disp_y
        new_vel_x = curr_vel_x + accel_pair[0]
        new_vel_y = curr_vel_y + accel_pair[1]
        is_out = False

        # Deslocamento horizontal
        for i in range(1, abs(disp_x) + 1):
            inc = -1
            mult = 1

            if disp_x < 0:
                mult = -1

            if self.matrix[curr_pos_x + i * mult][curr_pos_y] == 'F':
                return Node(curr_pos_x + i * mult, curr_pos_y, new_vel_x, new_vel_y, True, False)

            if self.matrix[curr_pos_x + i * mult][curr_pos_y] == 'X':
                is_out = True
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
                return Node(curr_pos_x, curr_pos_y + j * mult, new_vel_x, new_vel_y, True, False)

            if self.matrix[new_pos_x][curr_pos_y + j * mult] == 'X':
                is_out = True
                new_vel_y = new_vel_x = 0
                new_pos_y = curr_pos_y + j * mult + inc * mult

                break

        new_state = Node(new_pos_x, new_pos_y, new_vel_x, new_vel_y, False, is_out)
        #print(new_state)
        return new_state

    def build_states_from_node(self, state):
        nodes = list()

        n1 = self.next_state(state, (1, 1))
        nodes.append(n1)

        n2 = self.next_state(state, (1, -1))
        nodes.append(n2)

        n3 = self.next_state(state, (1, 0))
        nodes.append(n3)

        n4 = self.next_state(state, (-1, 1))
        nodes.append(n4)

        n5 = self.next_state(state, (-1, -1))
        nodes.append(n5)

        n6 = self.next_state(state, (0, -1))
        nodes.append(n6)

        n7 = self.next_state(state, (-1, 0))
        nodes.append(n7)

        n8 = self.next_state(state, (0, 0))
        nodes.append(n8)

        n9 = self.next_state(state, (0, 1))
        nodes.append(n9)

        return nodes

    def build_graph(self, initial_state, states_processed):
        adjs = list()
        adjs = self.build_states_from_node(initial_state)  # estados possiveis

        states_processed.append(initial_state)

        #for node in adjs:
        #    if node not in states_processed:
        #        states_processed.append(node)
        #        if node.get_is_out():
        #            self.graph.add_edge(initial_state, node, 25)
        #        else:
        #            self.graph.add_edge(initial_state, node, 1)
        #
        #        if not node.get_is_final_state():
        #            self.build_graph(node, states_processed)

        for node in adjs:
            if node.get_is_out():
                self.graph.add_edge(initial_state, node, 25)
            else:
                self.graph.add_edge(initial_state, node, 1)

            if not node.get_is_final_state() and node not in states_processed:
                self.build_graph(node, states_processed)

            states_processed.append(node)


#(matrix, start, final) = parser("../circuits/circuito1.txt")
#graph = Graph()
#
#r = Race(matrix, graph)
#
#initial_state = Node(1, 3, 0, 0, False, False)
#
#r.build_graph(initial_state, [])
#print(graph)
#