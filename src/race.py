from node import Node
from parser import parser

class Race:
    def __init__(self, matrix):
        self.matrix = matrix

    def nextState(self, state, acPair, matrix):
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
        newVelX = currVelX
        newVelY = currVelY

        #Deslocamento horizontal

        for i in range(1, abs(dispX)+1):
            inc = -1
            mult = 1
            
            if (dispX < 0):
                mult = -1
            
            if (matrix[currY][currX + i * mult] == 'F'):
                return Node(currX + i * mult, currY, newVelX, newVelY, True)
            
            if (matrix[currY][currX + i * mult] == 'X'):
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
                return Node(currX, currY + j * mult, newVelX, newVelY, True)

            if (matrix[currY + j * mult][newX] == 'X'):
                newVelY = newVelX = 0
                newY = currY + j * mult + inc * mult
                
                break

        newState = Node(newX, newY, newVelX, newVelY, False)
        return newState


mat = parser("../circuits/circuito1.txt")

r = Race([])
initialState = Node(7,3,5,1, False)
print(initialState)
newState = r.nextState(initialState, (-1, 1), mat)
print(newState)