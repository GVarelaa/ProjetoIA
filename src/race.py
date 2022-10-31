from node import Node
from parser import parser
from graph import Graph

class Race:
    def __init__(self, matrix, graph):
        self.matrix = matrix
        self.graph = graph

    def next_state(self, state, acel_pair, matrix):
        # Given an initial state, returns a resulting state
        # According to the choices of accelerations (acX, acY)
        # And to the matrix (map) of the circuit

        dispX = state.get_vel_x() + acel_pair[0]
        dispY = state.get_vel_y() + acel_pair[1]

        currX = state.get_pos_x()
        currY = state.get_pos_y()

        currVelX = state.get_vel_x()
        currVelY = state.get_vel_y()

        # Values if there are no obstacles in the way
        newX = currX + dispX
        newY = currY + dispY
        newVelX = currVelX
        newVelY = currVelY
        out = False

        #Deslocamento horizontal

        for i in range(1, abs(dispX)+1):
            inc = -1
            mult = 1
            
            if (dispX < 0):
                mult = -1
            
            if (matrix[currY][currX + i * mult] == 'F'):
                return Node(currX + i * mult, currY, newVelX, newVelY, True, out)
            
            if (matrix[currY][currX + i * mult] == 'X'):
                out = True
                newVelX = newVelY = 0
                newX = currX + i * mult + inc * mult
                
                break

        #Deslocamento vertical

        for j in range(1, abs(dispY)+1):
            inc = -1
            mult = 1
            
            if (dispY < 0):
                mult = -1
            
            if (matrix[currY + j * mult][newX] == 'F'):
                return Node(currX, currY + j * mult, newVelX, newVelY, True, out)

            if (matrix[currY + j * mult][newX] == 'X'):
                out = True
                newVelY = newVelX = 0
                newY = currY + j * mult + inc * mult
                
                break

        newState = Node(newX, newY, newVelX, newVelY, False, out)
        return newState


    def build_state(self, state, acel_pair, matrix):
        n = self.next_state(state, acel_pair, matrix)

        if n.get_out():
            self.graph.add_edge(state, n, 25)
        else:
            self.graph.add_edge(state, n, 1)

        return n

    def build_states_from_node(self, state, matrix):
        nodes = list()

        nodes.append(self.build_state(state, (1  , 1), matrix))
        nodes.append(self.build_state(state, (1  , -1), matrix))
        nodes.append(self.build_state(state, (1  , 0), matrix))
        nodes.append(self.build_state(state, (-1 , 1), matrix))
        nodes.append(self.build_state(state, (-1 , -1), matrix))
        nodes.append(self.build_state(state, (-1 , 0), matrix))
        nodes.append(self.build_state(state, (0  , 0), matrix))
        nodes.append(self.build_state(state, (0  , 1), matrix))
        nodes.append(self.build_state(state, (0  , -1), matrix))

        return nodes

    def build_graph(self, initial_state):
        nodes = list()
        nodes += self.build_states_from_node(initial_state, self.matrix)

        while nodes is not Empty:







mat = parser("../circuits/circuito1.txt")

r = Race([])
initialState = Node(7,3,5,1, False)
print(initialState)
newState = r.nextState(initialState, (-1, 1), mat)
print(newState)