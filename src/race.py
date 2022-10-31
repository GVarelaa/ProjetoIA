from node import Node
from parser import parser
from graph import Graph

class Race:
    def __init__(self, matrix, graph):
        self.matrix = matrix
        self.graph = graph

    def next_state(self, state, acel_pair):
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

        if(newY >= len(matrix) or newX >= len(matrix[0])):
            return None

        newVelX = state.get_vel_x() + acel_pair[0]
        newVelY = state.get_vel_y() + acel_pair[1]
        out = False

        #Deslocamento horizontal

        for i in range(1, abs(dispX)+1):
            inc = -1
            mult = 1
            
            if (dispX < 0):
                mult = -1
            
            if (currY < len(matrix) and (currX + i * mult) < len(matrix[0]) and self.matrix[currY][currX + i * mult] == 'F'):
                return Node(currX + i * mult, currY, newVelX, newVelY, True, out)
            
            if (currY < len(matrix) and (currX + i * mult) < len(matrix[0]) and self.matrix[currY][currX + i * mult] == 'X'):
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
            
            if (self.matrix[currY + j * mult][newX] == 'F'):
                return Node(currX, currY + j * mult, newVelX, newVelY, True, out)

            if (self.matrix[currY + j * mult][newX] == 'X'):
                out = True
                newVelY = newVelX = 0
                newY = currY + j * mult + inc * mult
                
                break


        print(newVelX, newVelY)
        newState = Node(newX, newY, newVelX, newVelY, False, out)
        print(newState)
        return newState


    def build_state(self, state, acel_pair):
        n = self.next_state(state, acel_pair)

        if n is not None and n.get_out():
            self.graph.add_edge(state, n, 25)
        elif n is not None:
            self.graph.add_edge(state, n, 1)

        return n

    def build_states_from_node(self, state):
        nodes = list()

        n1 = self.build_state(state, (1  , 1))
        if n1 is not None:
            nodes.append(n1)

        n2 = self.build_state(state, (1  , -1))
        if n2 is not None:
            nodes.append(n2)

        n3 = self.build_state(state, (1  , 0))
        if n3 is not None:
            nodes.append(n3)

        n4 = self.build_state(state, (-1 , 1))
        if n4 is not None:
            nodes.append(n4)

        n5 = self.build_state(state, (-1 , -1))
        if n5 is not None:
            nodes.append(n5)

        n6 = self.build_state(state, (0  , -1))
        if n6 is not None:
            nodes.append(n6)

        n7 = self.build_state(state, (-1 , 0))
        if n7 is not None:
            nodes.append(n7)

        #n8 = self.build_state(state, (0  , 0))
        #if n8 is not None:
        #    nodes.append(n8)

        n9 = self.build_state(state, (0  , 1))
        if n9 is not None:
            nodes.append(n9)

        return nodes

    def build_graph(self, initial_state):
        nodes = list()
        nodes += self.build_states_from_node(initial_state)

        for node in nodes:
            nodes += self.build_states_from_node(node)
            #print(nodes)







(matrix, start, final) = parser("../circuits/circuito1.txt")
graph = Graph()

r = Race(matrix, graph)

initial_state = Node(1,3,0,0, False, False)

r.build_graph(initial_state)

