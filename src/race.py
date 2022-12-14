import math
from enum import Enum

from node import Node
from parser import parser
from graph import Graph
import position_calculator
from copy import deepcopy
import drawer
import matplotlib.pyplot as plt


class Race:
    def __init__(self, matrix, start, end):
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
        return str(self.matrix) + str(self.graph)

    @staticmethod
    def next_state(state, accel_pair, mat):
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
        matrix = deepcopy(self.matrix)
        y_max = len(matrix)

        for node in path:
            pos_x = node.pos[0] - 0.5
            pos_y = y_max - node.pos[1] - 0.5
            matrix[int(pos_y)][int(pos_x)] = 'O'

        print_mat(matrix)

    def expand_state(self, state, mat):
        nodes = list()
        found = False
        accelerations = [(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (0, -1), (-1, 0), (0,0), (0,1)]

        for end in self.end:
            if state.pos == end.pos:
                found = True

        if not found:
            for accel in accelerations:
                nodes.append((self.next_state(state, accel, mat), accel))

        return nodes

    @staticmethod
    def calculate_shorter_distance(curr_state, pos_list):
        distance = math.inf

        for final_state in pos_list:
            temp = math.dist(curr_state.pos, final_state.pos)
            if temp < distance:
                distance = temp

        return distance

    def build_graph(self, mat=None, initial_state=None, end=None):
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
        path, cost, pos_visited = self.graph.DFS(initial_state, self.end, path=[], visited=set(), pos_visited=[])
        return path, cost, pos_visited

    def BFS_solution(self, initial_state):
        path, cost, pos_visited = self.graph.BFS(initial_state, self.end)
        return path, cost, pos_visited

    def a_star_solution(self, initial_state, type):
        path, cost, pos_visited = self.graph.a_star(initial_state, self.end, type)
        return path, cost, pos_visited

    def greedy_solution(self, initial_state, type):
        path, cost, pos_visited = self.graph.greedy(initial_state, self.end, type)
        return path, cost, pos_visited

    def check_win(self, players):
        for player in players:
            for end in self.end:
                if player.pos == end.pos:
                    return True

        return False

    def multiplayer(self):
        # paths ,costs
        players_states = deepcopy(self.start)
        matrix = deepcopy(self.matrix)

        paths = dict()
        for i in range(len(players_states)):
            paths[i] = list()

        while not self.check_win(players_states):
            for i in range(len(players_states)):
                players_states[i] = self.play(players_states[i], matrix, self.player_algorithms[i])
                paths[i].append(players_states[i])

                drawer.show_multiplayer_paths(paths, matrix)

    def play(self, player, matrix, algorithm):
        self.build_graph(matrix, player, self.end)
        path = list()
        match algorithm:
            case 1:
                path, cost, all_visited = self.graph.DFS(player, self.end)
            case 2:
                path, cost, all_visited = self.graph.BFS(player, self.end)
            case 3:
                path, cost, all_visited = self.graph.greedy(player, self.end, "distance")
            case 4:
                path, cost, all_visited = self.graph.a_star(player, self.end, "distance")
            case 5:
                return

        #print(path)
        update_mat(player.pos, path[1].pos, matrix)
        print_mat(matrix)

        return path[1]


def update_mat(begin, end, mat):
    mat_begin_row = len(mat) - math.floor(begin[1]) - 1
    mat_begin_collumn = math.floor(begin[0])
    mat_end_row = len(mat) - math.floor(end[1]) - 1
    mat_end_collumn = math.floor(end[0])

    mat[mat_begin_row][mat_begin_collumn] = '-'
    mat[mat_end_row][mat_end_collumn] = 'P'


def all_true(list):
    flag = True

    for bool in list:
        if not bool:
            return False

    return True


def utility_value(node, final_nodes):
    dist_to_obj = Race.calculate_shorter_distance(node, final_nodes)
    if dist_to_obj == 0:
        return math.inf
    else:
        return -dist_to_obj + node.vel[0]**2 + node.vel[1]**2
    # TODO


def print_mat(mat):
    string = ""
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            string += str(mat[i][j]) + " "
        string += "\n"

    print(string)
