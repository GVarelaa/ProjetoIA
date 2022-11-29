import math
from enum import Enum


class DispResult(Enum):
    CRASH = 1
    ADVANCE = 2
    FINISH = 3


def isInt(num):
    return math.floor(num) == num


# Example: nextInt(3) = 4
#          nextInt(2.5) = 3
def nextInt(num):
    if isInt(num):
        return num + 1
    else:
        return math.ceil(num)


# Example: lastInt(3) = 2
#          nextInt(2.5) = 2
def lastInt(num):
    if isInt(num):
        return num - 1
    else:
        return math.floor(num)


def calculateNextBorderPosition(currentPos, disp):
    if disp[1] == 0:  # Horizontal displacement
        if disp[0] < 0:
            return (lastInt(currentPos[0]), currentPos[1])
        elif disp[0] > 0:
            return (nextInt(currentPos[0]), currentPos[1])

    elif disp[0] == 0:  # Vertical displacement
        if disp[1] < 0:
            return (currentPos[0], lastInt(currentPos[1]))
        elif disp[1] > 0:
            return (currentPos[0], nextInt(currentPos[1]))

    grad = disp[1] / disp[0]  # Gradient

    # Calculate next X value
    if (disp[0] < 0):  # To the left
        nextValueHoriz = lastInt(currentPos[0])
    else:  # To the right
        nextValueHoriz = nextInt(currentPos[0])

    inc = nextValueHoriz - currentPos[0]

    auxPos = (currentPos[0] + inc, currentPos[1] + grad * inc)  # Calculate f(nextValueHoriz)

    # Upward disp
    if (disp[1] > 0 and auxPos[1] > nextInt(
            currentPos[1])):  # If f(nextValueHoriz) is greater than upper limit of square
        x = (nextInt(currentPos[1]) - currentPos[1] + currentPos[0] * grad) / grad  # Formula: x = (y-b+a*m)/m
        return (x, nextInt(currentPos[1]))

    # Downward disp
    elif (disp[1] < 0 and auxPos[1] < lastInt(
            currentPos[1])):  # If f(nextValueHoriz) is less than upper limit of square
        x = (lastInt(currentPos[1]) - currentPos[1] + currentPos[0] * grad) / grad  # Formula: x = (y-b+a*m)/m
        return (x, lastInt(currentPos[1]))

    else:
        return auxPos


# Get the object in that map position
def getMapObject(position, map):
    mapPosition = (math.floor(position[0]), math.floor(position[1]))
    matrixLine = len(map) - mapPosition[1] - 1
    matrixColumn = mapPosition[0]
    return map[matrixLine][matrixColumn]


# Get middle position of the next square, given borderPosition and displacement
def getMiddlePosition(borderPosition, displ):
    if isInt(borderPosition[1]):  # Case (float, int)
        if displ[0] == 0:  # Vertical motion
            return (borderPosition[0], borderPosition[1] + displ[1] / (abs(displ[1]) * 2))
        else:
            return (math.floor(borderPosition[0]) + 0.5, borderPosition[1] + (displ[1] / (abs(displ[1]) * 2)))
    else:  # Case (int, float)
        if displ[1] == 0:  # Horizontal motion
            return (borderPosition[0] + displ[0] / (abs(displ[0]) * 2), borderPosition[1])
        else:
            return (borderPosition[0] + (displ[0] / (abs(displ[0]) * 2)), math.floor(borderPosition[1]) + 0.5)


def calculateDispResult(borderPosition, displ, map):
    if isInt(borderPosition[0]) and isInt(borderPosition[1]):  # Esquina
        if displ[0] < 0 and displ[1] < 0:  # esquerda baixo
            firstPoint = (borderPosition[0] - 0.5, borderPosition[1] + 0.5)  # Can block displacement
            secondPoint = (borderPosition[0] + 0.5, borderPosition[1] - 0.5)  # Can block displacement
            thirdPoint = (borderPosition[0] - 0.5, borderPosition[1] - 0.5)  # Next position block

        if displ[0] < 0 and displ[1] > 0:  # esquerda cima
            firstPoint = (borderPosition[0] - 0.5, borderPosition[1] - 0.5)
            secondPoint = (borderPosition[0] + 0.5, borderPosition[1] + 0.5)
            thirdPoint = (borderPosition[0] - 0.5, borderPosition[1] + 0.5)

        if displ[0] > 0 and displ[1] < 0:  # direita baixo
            firstPoint = (borderPosition[0] + 0.5, borderPosition[1] + 0.5)
            secondPoint = (borderPosition[0] - 0.5, borderPosition[1] - 0.5)
            thirdPoint = (borderPosition[0] + 0.5, borderPosition[1] - 0.5)

        if displ[0] > 0 and displ[1] > 0:  # direita cima
            firstPoint = (borderPosition[0] - 0.5, borderPosition[1] + 0.5)
            secondPoint = (borderPosition[0] + 0.5, borderPosition[1] - 0.5)
            thirdPoint = (borderPosition[0] + 0.5, borderPosition[1] + 0.5)

        objFirstPoint = getMapObject(firstPoint, map)
        objSecondPoint = getMapObject(secondPoint, map)
        objThirdPoint = getMapObject(thirdPoint, map)

        if objFirstPoint == 'X' or objSecondPoint == 'X' or objThirdPoint == 'X':
            return DispResult.CRASH
        elif objThirdPoint == 'F':
            return DispResult.FINISH
        else:
            return DispResult.ADVANCE

    # Case (int, float) or (float, int)
    middlePosition = getMiddlePosition(borderPosition, displ)

    # Get object inside the square
    objInSquare = getMapObject(middlePosition, map)

    if objInSquare == 'X':
        return DispResult.CRASH
    elif objInSquare == 'F':
        return DispResult.FINISH
    else:
        return DispResult.ADVANCE


def calculateStopPosition(currentPos, disp, map):
    # Partindo da posição, até chegar à posição final, procura a próxima interseção com uma fronteira
    if disp == (0,0):
        return (currentPos, DispResult.ADVANCE)
    i = 0
    while i < abs(disp[0]) + abs(disp[1]):
        currentPos = calculateNextBorderPosition(currentPos, disp)  # Calculate position when leaving the square
        displacementResult = calculateDispResult(currentPos, disp,
                                                 map)  # Calculate object in next Square or Squares

        if isInt(currentPos[0]) and isInt(currentPos[1]) and displacementResult == DispResult.CRASH:
            finalPosition = (
                currentPos[0] - (disp[0] / abs(disp[0])) * 0.5, currentPos[1] - (disp[1] / abs(disp[1])) * 0.5)
            return (finalPosition, displacementResult)

        if isInt(currentPos[0]) and isInt(currentPos[1]) and displacementResult == DispResult.FINISH:
            finalPosition = (
                currentPos[0] + (disp[0] / abs(disp[0])) * 0.5, currentPos[1] + (disp[1] / abs(disp[1])) * 0.5)
            return (finalPosition, displacementResult)

        if (displacementResult == DispResult.CRASH):
            finalPosition = getMiddlePosition(currentPos, (-1 * disp[0], -1 * disp[1]))
            return (finalPosition, displacementResult)

        if (displacementResult == DispResult.FINISH):
            finalPosition = getMiddlePosition(currentPos, disp)
            return (finalPosition, displacementResult)

        if isInt(currentPos[0]) and isInt(currentPos[1]):
            i += 1
        i += 1

    finalPosition = getMiddlePosition(currentPos, disp)
    displacementResult = DispResult.ADVANCE
    return (finalPosition, displacementResult)