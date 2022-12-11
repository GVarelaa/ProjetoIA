import math
from enum import Enum

from node import Node
from parser import parser
from graph import Graph
import position_calculator
from copy import deepcopy


class Race:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.graph = Graph()
        self.start = list()
        self.end = list()

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

    def build_graph(self):
        states = deepcopy(self.start)

        visited = deepcopy(self.start)

        while states:
            state = states.pop()
            expansion = self.expand_state(state, self.matrix)

            self.graph.add_heuristic(state, Race.calculate_shorter_distance(state, self.end), "distance")  # distância às posiçoes finais
            self.graph.add_heuristic(state, math.sqrt(state.vel[0] ** 2 + state.vel[1] ** 2), "velocity")  # velocidade atual

            for (e,accel) in expansion:
                if e.crashed:
                    e.crashed = False
                    self.graph.add_edge(state, e, 25)
                else:
                    self.graph.add_edge(state, e, 1)

                if e not in visited:
                    states.append(e)
                    visited.append(e)

    def DFS_solution(self, debug):
        res = self.graph.DFS(self.start[0], self.end, deepcopy(self.matrix), debug, path=[], visited=set())
        return res

    def BFS_solution(self):
        res = self.graph.BFS(self.start[0], self.end)
        path, cost = res
        self.graph.print_result(deepcopy(self.matrix), path)
        return res

    def a_star_solution(self, type):
        res = self.graph.a_star(self.start[0], self.end, type)
        path, cost = res
        self.graph.print_result(deepcopy(self.matrix), res)
        return res

    def greedy_solution(self, type):
        res = self.graph.greedy(self.start[0], self.end, type)
        path, cost = res
        self.graph.print_result(deepcopy(self.matrix), res)
        return res

    def multiplayer(self):
        # paths ,costs
        players_states = deepcopy(self.start)
        paths_found = list()    # Se já chegou ao fim da pista
        parents = list()
        for state in players_states:
            paths_found.append(False)
            dic = dict()
            dic[state] = None
            parents.append(dic)
        print(players_states)

        while not all_true(paths_found):
            for i in range(len(players_states)):
                if paths_found[i] == False:
                    paths_found[i], players_states[i] = self.play(players_states[i], parents[i], self.matrix)
                    if paths_found[i] == True:
                        mat_row = len(self.matrix) - math.floor(players_states[i].pos[1]) - 1
                        mat_collumn = math.floor(players_states[i].pos[0])
                        self.matrix[mat_row][mat_collumn] = 'F'

            # Joga jogador 1
            # Joga jogador 2
            # ...
        i=0
        for p in parents:
            path = []
            node = players_states[i]
            path.append(node)
            while p[node] is not None:
                path.append(p[node])
                node = p[node]
            path.reverse()
            print(path)
            i+=1
        return ([], [])

    def play(self, state, parents, mat):
        next_pos = self.expand_state(state, mat)
        max_pos = next_pos[0]
        max = utility_value(next_pos[0][0], self.end)

        for i in range(len(next_pos)):
            ut_value = utility_value(next_pos[i][0], self.end)
            if ut_value > max:
                max = ut_value
                max_pos = next_pos[i]

        update_mat(state.pos, max_pos[0].pos, mat)
        parents[max_pos[0]] = state
        print_mat(mat)
        if max == math.inf:
            return True, max_pos[0]
        else:
            return False, max_pos[0]

    def mini_max(self, depth, player, player_states, playerIndex, mat):
        if player == 1: # Max is playing
            next_states = self.expand_state(player_states[playerIndex], mat)
            max_utility = -math.inf
            for state in next_states:
                if depth == 0:
                    utility = utility_value(state[0], self.end)
                else:
                    st_copy = deepcopy(player_states) # Copy of the states
                    st_copy[playerIndex] = state # Updating player state
                    mat_copy = deepcopy(mat)
                    update_mat(player_states[playerIndex].pos, state[0].pos)
                    utility = self.mini_max(depth-1, 0, st_copy, (playerIndex+1)%len(player_states), mat)
                if utility > max_utility:
                    max_utility = utility
                    next_state = state
            optimal_utility = max_utility
        elif player == 0: # Min is playing
            next_states = None
            min_utility = math.inf
            for state in next_states:
                st_copy = deepcopy(player_states)  # Copy of the states
                st_copy[playerIndex] = state  # Updating player state
                mat_copy = deepcopy(mat)
                update_mat(player_states[playerIndex].pos, state[0].pos)
                utility = self.mini_max(depth - 1, 0, st_copy, (playerIndex + 1) % len(player_states), mat)
                if utility < min_utility:
                    min_utility = utility
                    next_state = state
                optimal_utility = min_utility

        return optimal_utility


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
        if bool == False:
            return False
    return flag


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