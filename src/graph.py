import math
from node import Node

class Graph:
    #construtor de classe
    def __init__(self):
        self.nodes = []     # lista com os nodos do grafo
        self.graph = {}     # dicionario do grafo
        self.h = {}         # dicionario com heurisiticas

    def __str__(self):
        string = ""
        for key in self.graph.keys():
            string = string + str(key) + ": \n"
            for node in self.graph[key]:
                string += "     " + str(node) + "\n"

        return string

    def __repr__(self):
        string = ""
        for key in self.graph.keys():
            string = string + "Nodo " + str(key) + ": " + str(self.graph[key]) + "\n"

        return string

    def get_node_by_pos(self, pos):
        for node in self.nodes:
            if node.get_pos() == pos:
                return node

    def add_edge(self, node1, node2, weight):
        if node1 not in self.nodes:
            self.nodes.append(node1)
            self.graph[node1] = set()

        if node2 not in self.nodes:
            self.nodes.append(node2)
            self.graph[node2] = set()

        self.graph[node1].add((node2, weight))

    def get_arc_cost(self, node1, node2):
        if (node1 == node2):
            return 0

        custoT = math.inf
        set = self.graph[node1]

        for (name, weight) in set:
            if (name == node2):
                custoT = weight

        return custoT

    def calcula_custo(self, caminho):
        custo = 0
        i = 0

        while i + 1 < len(caminho):
            custo = custo + self.get_arc_cost(caminho[i], caminho[i + 1])
            i = i + 1

        return custo

    def procura_DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            # calcular o custo do caminho função calcula custo
            custoT = self.calcula_custo(path)
            return (path, custoT)

        for (adjacente, peso) in self.graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado

        path.pop()  # se nao encontra, remover o que está no caminho
        return None





