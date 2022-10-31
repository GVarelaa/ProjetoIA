from node import Node
from parser import parser
from graph import Graph

class Race:
    def __init__(self, matrix, graph):
        self.matrix = matrix
        self.graph = graph

    def next_state(self, state, acPair):
        # Given an initial state, returns a resulting state
        # According to the choices of accelerations (acX, acY)
        # And to the matrix (map) of the circuit

        dispX = state.get_vel_x() + acPair[0]
        dispY = state.get_vel_y() + acPair[1]

        currX = state.get_pos_x()
        currY = state.get_pos_y()

        currVelX = state.get_vel_x()
        currVelY = state.get_vel_y()

        # Values if there are no obstacles in the way
        newX = currX + dispX
        newY = currY + dispY
        newVelX = currVelX + acPair[0]
        newVelY = currVelY + acPair[1]
        out = False

        # Deslocamento horizontal

        for i in range(1, abs(dispX) + 1):
            inc = -1
            mult = 1

            if (dispX < 0):
                mult = -1

            if (matrix[currX + i * mult][currY] == 'F'):
                return Node(currX + i * mult, currY, newVelX, newVelY, True, False)

            if (matrix[currX + i * mult][currY] == 'X'):
                out = True
                newVelX = newVelY = 0
                newX = currX + i * mult + inc * mult

                break

        # Deslocamento vertical

        for j in range(1, abs(dispY) + 1):
            inc = -1
            mult = 1

            if (dispY < 0):
                mult = -1

            if (matrix[newX][currY + j * mult] == 'F'):
                return Node(currX, currY + j * mult, newVelX, newVelY, True, False)

            if (matrix[newX][currY + j * mult] == 'X'):
                out = True
                newVelY = newVelX = 0
                newY = currY + j * mult + inc * mult

                break


        newState = Node(newX, newY, newVelX, newVelY, False, out)
        print(newState)
        return newState

    def build_states_from_node(self, state):
        nodes = list()

        n1 = self.next_state(state, (1  , 1))
        nodes.append(n1)

        n2 = self.next_state(state, (1  , -1))
        nodes.append(n2)

        n3 = self.next_state(state, (1  , 0))
        nodes.append(n3)

        n4 = self.next_state(state, (-1 , 1))
        nodes.append(n4)

        n5 = self.next_state(state, (-1 , -1))
        nodes.append(n5)

        n6 = self.next_state(state, (0  , -1))
        nodes.append(n6)

        n7 = self.next_state(state, (-1 , 0))
        nodes.append(n7)

        n8 = self.next_state(state, (0  , 0))
        nodes.append(n8)

        n9 = self.next_state(state, (0  , 1))
        nodes.append(n9)

        return nodes

    def build_graph(self, initial_state, states_processed):
        nodes = list()
        nodes = self.build_states_from_node(initial_state) # estados possiveis

        states_processed.append(initial_state)

        for node in nodes:
            if node not in states_processed:
                states_processed.append(node)
                if node.get_out() == True:
                    print("aqui\n")
                    self.graph.add_edge(initial_state, node, 25)
                else:
                    self.graph.add_edge(initial_state, node, 1)

                if node.get_final_state() == False:
                    self.build_graph(node, states_processed)


(matrix, start, final) = parser("../circuits/circuito1.txt")
graph = Graph()

r = Race(matrix, graph)

initial_state = Node(1 ,3, 0, 0, False, False)

r.build_graph(initial_state, [])
print(graph)

