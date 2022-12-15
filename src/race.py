import math
from enum import Enum
from time import sleep

from node import Node
from parser import parser
from graph import Graph
import position_calculator
from copy import deepcopy
import drawer
import math
import matplotlib.pyplot as plt


class Race:
    def __init__(self, matrix, start, end):
        """

        :param matrix:
        :param start:
        :param end:
        """
        self.matrix = matrix
        self.graph = Graph()
        self.start = list()
        self.end = list()
        self.player_algorithms = dict()

        for pos in start:
            self.start.append(Node(pos, (0, 0), False))

        for pos in end:
            self.end.append(Node(pos, (-1, -1), False))

    def __str__(self):
        """

        :return:
        """
        return str(self.matrix) + str(self.graph)

    @staticmethod
    def next_state(state, accel_pair, mat):
        """
        Calcula o próximo estado
        :param state: Estado atual
        :param accel_pair: Aceleração
        :param mat: matriz
        :return: Nodo
        """
        disp = (state.vel[0] + accel_pair[0], state.vel[1] + accel_pair[1])

        (new_position, action) = position_calculator.calculate_stop_position(state.pos, disp, mat)

        new_vel = (state.vel[0] + accel_pair[0], state.vel[1] + accel_pair[1])

        if action == position_calculator.DispResult.CRASH:
            new_vel = (0, 0)

        is_crashed = False
        if action == position_calculator.DispResult.CRASH:
            is_crashed = True

        return Node(new_position, new_vel, is_crashed)

    def print_result(self, path):
        """
        Imprime o resultado
        :param path: Caminho
        :return:
        """
        matrix = deepcopy(self.matrix)
        y_max = len(matrix)

        for node in path:
            pos_x = node.pos[0] - 0.5
            pos_y = y_max - node.pos[1] - 0.5
            matrix[int(pos_y)][int(pos_x)] = 'O'

        print_mat(matrix)

    def expand_state(self, state, mat):
        """
        Cria uma lista de nodos
        :param state: Estado Atual
        :param mat: Matriz
        :return: Nodos
        """
        nodes = list()
        found = False
        accelerations = [(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (0, -1), (-1, 0), (0,0), (0,1)]

        for end in self.end:
            if state.pos == end.pos:
                found = True

        if not found:
            for accel in accelerations:
                s = (self.next_state(state, accel, mat), accel)
                nodes.append(s)
        return nodes

    @staticmethod
    def calculate_shorter_distance(curr_state, pos_list):
        """
        Calcula a menor distancia
        :param curr_state: Estado Atual
        :param pos_list: Lista de Posições
        :return: Distancia
        """
        distance = math.inf

        for final_state in pos_list:
            temp = math.dist(curr_state.pos, final_state.pos)
            if temp < distance:
                distance = temp

        return distance

    def build_graph(self, mat=None, initial_state=None, end=None):
        """
        Constroi um grafo
        :param mat: Matriz
        :param initial_state: Estado inicial
        :param end: Posição Final
        :return:
        """
        if mat is None:
            mat = self.matrix

        if initial_state is None:
            initial_state = self.start[0]

        if end is None:
            end = self.end

        states = [deepcopy(initial_state)]
        visited = [deepcopy(initial_state)]

        while states:
            state = states.pop()
            expansion = self.expand_state(state, mat)

            for (e,accel) in expansion:
                if e.crashed:
                    e.crashed = False
                    self.graph.add_edge(state, e, 25)
                else:
                    self.graph.add_edge(state, e, 1)

                if e not in visited:
                    states.append(e)
                    visited.append(e)

            self.graph.add_heuristic(state, Race.calculate_shorter_distance(state, end),
                                     "distance")  # distância às posiçoes finais
            self.graph.add_heuristic(state, math.sqrt(state.vel[0] ** 2 + state.vel[1] ** 2),
                                     "velocity")  # velocidade atual

    def DFS_solution(self, initial_state):
        """
        Calcula a solução do algoritmo DFS a partir de um estado inicial
        :param initial_state: Estado Inicial
        :return: Caminho, Custo e Posições vistadas
        """
        path, cost, pos_visited = self.graph.DFS(initial_state, self.end, path=[], visited=set(), pos_visited=[])
        return path, cost, pos_visited

    def BFS_solution(self, initial_state):
        """
        Calcula a solução do algoritmo BFS a partir de um estado inicial
        :param initial_state: Estado Inicial
        :return: Caminho, Custo e Posições vistadas
        """
        path, cost, pos_visited = self.graph.BFS(initial_state, self.end)
        return path, cost, pos_visited

    def a_star_solution(self, initial_state, type):
        """
        Calcula a solução do algoritmo A-Star a partir de um estado inicial
        :param initial_state: Estado Inicial
        :param type: Tipo
        :return: Caminho, Custo e Posições visitadas
        """
        path, cost, pos_visited = self.graph.a_star(initial_state, self.end, type)
        return path, cost, pos_visited

    def greedy_solution(self, initial_state, type):
        """
        Calcula a solução do algoritmo Greedy a partir de um estado inicial
        :param initial_state: Estado Inicial
        :param type: Tipo
        :return: Caminho, Custo e Posições Visitadas
        """
        path, cost, pos_visited = self.graph.greedy(initial_state, self.end, type)
        return path, cost, pos_visited

    def check_win(self, players):
        """
        Verifica se um jogador já chegou ao final
        :param players: Lista de jogadores
        :return: Bool
        """
        for player in players:
            for end in self.end:
                if player.pos == end.pos:
                    return True

        return False

    def multiplayer(self):
        """
        Executa o modo multiplayer
        :return:
        """
        # paths ,costs
        players_states = deepcopy(self.start)
        matrix = deepcopy(self.matrix)

        paths = dict()
        dist = list()
        for i in range(len(players_states)):
            paths[i] = list()
            dist.append(math.inf)

        while not self.check_win(players_states):
            for i in range(len(players_states)):
                r = self.play(players_states[i], matrix, self.player_algorithms[i])
                list_checked = list()
                list_checked.append(i)

                if r is None:
                    next_states = self.expand_state(players_states[i], matrix)
                    next_pos = higher_vel_state(next_states)
                    update_mat(players_states[i].pos, next_pos.pos, matrix)
                else:
                    next_pos, dist[i] = r

                players_states[i] = next_pos

                paths[i].append(players_states[i])

            drawer.show_multiplayer_paths(paths, matrix)
            print_mat(matrix)

            sleep(0.55)

    def play(self, player, matrix, algorithm):
        """
        Executa uma jogada
        :param player: Jogador
        :param matrix: Matriz
        :param algorithm: Algoritmo
        :return: Resultado do algoritmo
        """
        self.graph = Graph()
        self.build_graph(matrix, player, self.end)
        path = list()
        match algorithm:
            case 1:
                 r = self.graph.DFS(player, self.end)
            case 2:
                r = self.graph.BFS(player, self.end)
            case 3:
                r = self.graph.greedy(player, self.end, "distance")
            case 4:
                r = self.graph.a_star(player, self.end, "distance")
            case 5:
                return
        if r is not None:
            path, cost, all_visited = r
        else:
            return r

def get_vel_value(velocity):
    """
    Obtem o valor da velocidade
    :param velocity: Velocidade
    :return: Velocidade
    """
    return math.sqrt(velocity[0]**2 + velocity[1]**2)

def higher_vel_state(states):
    """
    Devolve o estado com maior velociadade
    :param states: Lista de estados
    :return: Estado com maior velocidade
    """
    higher = states[0][0]

    for state in states:
        if get_vel_value(higher.vel) < get_vel_value(state[0].vel):
            higher = state[0]

    return higher
def update_mat(begin, end, mat):
    """
    Atualiza a matriz
    :param begin: Posição inicial
    :param end: Posição Final
    :param mat: Matriz
    :return:
    """
    mat_begin_row = len(mat) - math.floor(begin[1]) - 1
    mat_begin_collumn = math.floor(begin[0])
    mat_end_row = len(mat) - math.floor(end[1]) - 1
    mat_end_collumn = math.floor(end[0])

    mat[mat_begin_row][mat_begin_collumn] = '-'
    mat[mat_end_row][mat_end_collumn] = 'P'


def all_true(list):
    """
    Verifica se a lista tem tudo a Verdadeiro
    :param list: Lista
    :return: Bool
    """
    flag = True

    for bool in list:
        if not bool:
            return False

    return True


def utility_value(node, final_nodes):
    """
    Distancia ate um objeto
    :param node: Nodo
    :param final_nodes: Nodos finais
    :return: Distancia
    """
    dist_to_obj = Race.calculate_shorter_distance(node, final_nodes)
    if dist_to_obj == 0:
        return math.inf
    else:
        return -dist_to_obj + node.vel[0]**2 + node.vel[1]**2
    # TODO


def print_mat(mat):
    """
    Imprime a Matriz
    :param mat: Matriz
    :return:
    """
    string = ""
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            string += str(mat[i][j]) + " "
        string += "\n"

    print(string)
