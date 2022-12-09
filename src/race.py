import math
from enum import Enum

from node import Node
from parser import parser
from graph import Graph
import position_calculator
from copy import deepcopy


class Race:
    def __init__(self, matrix, startPos, end):
        self.matrix = matrix
        self.graph = Graph()
        self.start = list()
        for pos in startPos:
            self.start.append(Node(pos, (0,0), False))
        self.end = list()

        for pos in end:
            self.end.append(Node(pos, (-1, -1), False))

    def __str__(self):
        return str(self.matrix) + str(self.graph)

    def next_state(self, state, accel_pair):
        disp = (state.vel[0] + accel_pair[0], state.vel[1] + accel_pair[1])

        (new_position, action) = position_calculator.calculate_stop_position(state.pos, disp, self.matrix)

        new_vel = (state.vel[0] + accel_pair[0], state.vel[1] + accel_pair[1])

        if action == position_calculator.DispResult.CRASH:
            new_vel = (0, 0)

        is_crashed = False
        if action == position_calculator.DispResult.CRASH:
            is_crashed = True

        return Node(new_position, new_vel, is_crashed)

    def expand_state(self, state):
        nodes = list()
        found = False
        accelerations = [(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (0, -1), (-1, 0), (0,0), (0,1)]

        for end in self.end:
            if state.pos == end.pos:
                found = True

        if not found:
            for accel in accelerations:
                nodes.append(self.next_state(state, accel))

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
            expansion = self.expand_state(state)

            self.graph.add_heuristic(state, Race.calculate_shorter_distance(state, self.end))

            for e in expansion:
                if e.crashed:
                    e.crashed = False
                    self.graph.add_edge(state, e, 25)
                else:
                    self.graph.add_edge(state, e, 1)

                if e not in visited:
                    states.append(e)
                    visited.append(e)

    def DFS_solution(self, debug):
        res = self.graph.DFS(self.start, self.end, deepcopy(self.matrix), debug, path=[], visited=set())
        return res

    def BFS_solution(self):
        res = self.graph.BFS(self.start, self.end)
        path, cost = res
        self.graph.print_result(deepcopy(self.matrix), path)
        return res

    def a_star_solution(self):
        res = self.graph.a_star(self.start, self.end)
        path, cost = res
        self.graph.print_result(deepcopy(self.matrix), res)
        return res

    def greedy_solution(self):
        res = self.graph.greedy(self.start, self.end)
        path, cost = res
        self.graph.print_result(deepcopy(self.matrix), res)
        return res

    def multiplayer(self):
        paths, costs = self.graph.multiplayer(self.start, self.end)