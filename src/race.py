import math
from enum import Enum

from node import Node
from parser import parser
from graph import Graph
import position_calculator

class Race:
    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.graph = Graph()
        self.start = Node(start, (0,0), False, False, (0,0))
        self.end = list()

        for pos in end:
            self.end.append(Node(pos, (-1,-1), False, False, (0,0)))

    def __str__(self):
        return str(self.matrix) + str(self.graph)

    def next_state(self, state, accel_pair):
        disp = (state.vel[0] + accel_pair[0], state.vel[1] + accel_pair[1])
        (new_position, action) = position_calculator.calculateStopPosition(state.pos, disp, self.matrix)

        new_vel = (state.vel[0] + accel_pair[0], state.vel[1] + accel_pair[1])

        if action == position_calculator.DispResult.CRASH:
            new_vel = (0,0)

        is_crashed = False
        if disp == position_calculator.DispResult.CRASH:
            is_cashed = True

        is_finished = False
        if disp == position_calculator.DispResult.FINISH:
            is_finished = True

        return Node(new_position, new_vel, is_finished, is_crashed, accel_pair)


    def expand_state(self, state):
        nodes = list()

        for end in self.end:
            if state.pos == end.pos:
                return nodes

        n1 = self.next_state(state, (1, 1))
        if n1:
            nodes.append(n1)

        n2 = self.next_state(state, (1, -1))
        if n2:
            nodes.append(n2)

        n3 = self.next_state(state, (1, 0))
        if n3:
            nodes.append(n3)

        n4 = self.next_state(state, (-1, 1))
        if n4:
            nodes.append(n4)

        n5 = self.next_state(state, (-1, -1))
        if n5:
            nodes.append(n5)

        n6 = self.next_state(state, (0, -1))
        if n6:
            nodes.append(n6)

        n7 = self.next_state(state, (-1, 0))
        if n7:
            nodes.append(n7)

        n8 = self.next_state(state, (0, 0))
        if n8:
            nodes.append(n8)

        n9 = self.next_state(state, (0, 1))
        if n9:
            nodes.append(n9)

        return nodes

    def build_graph(self):
        states = [self.start]

        visited = [self.start]

        while states:
            state = states.pop()
            expansion = self.expand_state(state)

            for e in expansion:
                if e.crashed:
                    self.graph.add_edge(state, e, 25)
                else:
                    self.graph.add_edge(state, e, 1)

                if e not in visited:
                    states.append(e)
                    visited.append(e)




    def DFS_solution(self):
        res = self.graph.DFS(self.start, self.end, path = [], visited = set())
        return res

    def BFS_solution(self):
        res = self.graph.BFS(self.start, self.end)
        return res