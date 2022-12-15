import math
from enum import Enum


class DispResult(Enum):
    CRASH = 1
    ADVANCE = 2
    FINISH = 3


def is_int(num):
    """
    Verifica se é um inteiro
    :param num: Número
    :return: Bool
    """
    return math.floor(num) == num


# Example: nextInt(3) = 4
#          nextInt(2.5) = 3
def next_int(num):
    """
    Incrementa um número
    :param num: Número
    :return: Numero incrementado
    """
    if is_int(num):
        return num + 1
    else:
        return math.ceil(num)


# Example: lastInt(3) = 2
#          nextInt(2.5) = 2
def last_int(num):
    """
    Decremeneta um número
    :param num: Número
    :return: Número decrementado
    """
    if is_int(num):
        return num - 1
    else:
        return math.floor(num)

def calculate_next_border_position(current_pos, disp):
    """
    Calcula a borda da proxima posição
    :param current_pos: Posição Atual
    :param disp: Deslocamento
    :return: Posição
    """
    if disp[1] == 0:  # Horizontal displacement
        if disp[0] < 0:
            return last_int(current_pos[0]), current_pos[1]
        elif disp[0] > 0:
            return next_int(current_pos[0]), current_pos[1]

    elif disp[0] == 0:  # Vertical displacement
        if disp[1] < 0:
            return current_pos[0], last_int(current_pos[1])
        elif disp[1] > 0:
            return current_pos[0], next_int(current_pos[1])

    grad = disp[1] / disp[0]  # Gradient

    # Calculate next X value
    if disp[0] < 0:  # To the left
        next_value_horiz = last_int(current_pos[0])
    else:  # To the right
        next_value_horiz = next_int(current_pos[0])

    inc = next_value_horiz - current_pos[0]

    aux_pos = (current_pos[0] + inc, current_pos[1] + grad * inc)  # Calculate f(next_value_horiz)

    # Upward disp
    if disp[1] > 0 and aux_pos[1] > next_int(current_pos[1]):  # If f(next_value_horiz) is greater than upper limit of square
        x = (next_int(current_pos[1]) - current_pos[1] + current_pos[0] * grad) / grad  # Formula: x = (y-b+a*m)/m
        return x, next_int(current_pos[1])

    # Downward disp
    elif disp[1] < 0 and aux_pos[1] < last_int(current_pos[1]):  # If f(next_value_horiz) is less than upper limit of square
        x = (last_int(current_pos[1]) - current_pos[1] + current_pos[0] * grad) / grad  # Formula: x = (y-b+a*m)/m
        return x, last_int(current_pos[1])

    else:
        return aux_pos


# Get the object in that map position
def get_map_object(position, map):
    """
    Destaca uma posição no mapa
    :param position: Posição
    :param map: mapa
    :return: mapa
    """
    map_position = (math.floor(position[0]), math.floor(position[1]))
    matrix_line = len(map) - map_position[1] - 1
    matrix_column = map_position[0]
    return map[matrix_line][matrix_column]


# Get middle position of the next square, given border_position and displacement
def get_middle_position(border_position, displ):
    """
    Obtem a posição intemédia
    :param border_position: Posição da borda
    :param displ: Deslocamento
    :return: Posição
    """
    if is_int(border_position[1]):  # Case (float, int)
        if displ[0] == 0:  # Vertical motion
            return border_position[0], border_position[1] + displ[1] / (abs(displ[1]) * 2)
        else:
            return math.floor(border_position[0]) + 0.5, border_position[1] + (displ[1] / (abs(displ[1]) * 2))
    else:  # Case (int, float)
        if displ[1] == 0:  # Horizontal motion
            return border_position[0] + displ[0] / (abs(displ[0]) * 2), border_position[1]
        else:
            return border_position[0] + (displ[0] / (abs(displ[0]) * 2)), math.floor(border_position[1]) + 0.5


def calculate_disp_result(border_position, displ, map):
    """
    Calcula o resultado do deslocamento
    :param border_position: Posição da borda
    :param displ: Deslocamento
    :param map: mapa
    :return: POsição
    """
    if is_int(border_position[0]) and is_int(border_position[1]):  # Esquina
        if displ[0] < 0 and displ[1] < 0:  # esquerda baixo
            first_point = (border_position[0] - 0.5, border_position[1] + 0.5)  # Can block displacement
            second_point = (border_position[0] + 0.5, border_position[1] - 0.5)  # Can block displacement
            third_point = (border_position[0] - 0.5, border_position[1] - 0.5)  # Next position block

        if displ[0] < 0 and displ[1] > 0:  # esquerda cima
            first_point = (border_position[0] - 0.5, border_position[1] - 0.5)
            second_point = (border_position[0] + 0.5, border_position[1] + 0.5)
            third_point = (border_position[0] - 0.5, border_position[1] + 0.5)

        if displ[0] > 0 and displ[1] < 0:  # direita baixo
            first_point = (border_position[0] + 0.5, border_position[1] + 0.5)
            second_point = (border_position[0] - 0.5, border_position[1] - 0.5)
            third_point = (border_position[0] + 0.5, border_position[1] - 0.5)

        if displ[0] > 0 and displ[1] > 0:  # direita cima
            first_point = (border_position[0] - 0.5, border_position[1] + 0.5)
            second_point = (border_position[0] + 0.5, border_position[1] - 0.5)
            third_point = (border_position[0] + 0.5, border_position[1] + 0.5)

        obj_first_point = get_map_object(first_point, map)
        obj_second_point = get_map_object(second_point, map)
        obj_third_point = get_map_object(third_point, map)

        if obj_first_point == 'X' or obj_second_point == 'X' or obj_third_point == 'X' or obj_first_point == 'P' or obj_second_point == 'P' or obj_third_point == 'P':
            return DispResult.CRASH
        elif obj_third_point == 'F':
            return DispResult.FINISH
        else:
            return DispResult.ADVANCE

    # Case (int, float) or (float, int)
    middle_position = get_middle_position(border_position, displ)

    # Get object inside the square
    obj_in_square = get_map_object(middle_position, map)

    if obj_in_square == 'P' or obj_in_square == 'X':
        return DispResult.CRASH
    elif obj_in_square == 'F':
        return DispResult.FINISH
    else:
        return DispResult.ADVANCE


def calculate_stop_position(current_pos, disp, map):
    """
    Calcula a posição onde pára
    :param current_pos: Posição Atual
    :param disp: Deslocamento
    :param map: mapa
    :return: Posição e deslocamento
    """
    # Partindo da posição, até chegar à posição final, procura a próxima interseção com uma fronteira
    if current_pos is (2.5, 6.5):
        print('ola')
    if disp == (0, 0):
        return current_pos, DispResult.ADVANCE

    i = 0

    while i < abs(disp[0]) + abs(disp[1]):
        current_pos = calculate_next_border_position(current_pos, disp)  # Calculate position when leaving the square
        displacement_result = calculate_disp_result(current_pos, disp, map)  # Calculate object in next Square or Squares

        if is_int(current_pos[0]) and is_int(current_pos[1]) and displacement_result == DispResult.CRASH:
            final_position = (
                current_pos[0] - (disp[0] / abs(disp[0])) * 0.5, current_pos[1] - (disp[1] / abs(disp[1])) * 0.5)
            return final_position, displacement_result

        if is_int(current_pos[0]) and is_int(current_pos[1]) and displacement_result == DispResult.FINISH:
            final_position = (
                current_pos[0] + (disp[0] / abs(disp[0])) * 0.5, current_pos[1] + (disp[1] / abs(disp[1])) * 0.5)
            return final_position, displacement_result

        if displacement_result == DispResult.CRASH:
            final_position = get_middle_position(current_pos, (-1 * disp[0], -1 * disp[1]))
            return final_position, displacement_result

        if displacement_result == DispResult.FINISH:
            final_position = get_middle_position(current_pos, disp)
            return final_position, displacement_result

        if is_int(current_pos[0]) and is_int(current_pos[1]):
            i += 1

        i += 1

    final_position = get_middle_position(current_pos, disp)
    displacement_result = DispResult.ADVANCE
    return final_position, displacement_result
