from node import Node

class Graph:
    #construtor de classe
    def __init__(self):
        self.nodes = []     # lista com os nodos do grafo
        self.graph = {}     # dicionario do grafo
        self.h = {}         # dicionario com heurisiticas

    def __str__(self):
        string = ""
        for key in self.m_graph.keys():
            string = string + "Nodo " + str(key) + ": " + str(self.m_graph[key]) + "\n"

        return string

    def get_node_by_pos(self, pos):
        for node in self.nodes:
            if node.get_pos() == pos:
                return node

    def add_edge(self, node1, node2, weight):
        if node1 not in self.nodes:
            self.nodes.append(node1)
            self.graph[(node1.get_pos(), node1.get_vel())] = set()

        if node2 not in self.nodes:
            self.nodes.append(node2)
            self.graph[(node2.get_pos(), node2.get_vel())] = set()

        self.graph[(node1.get_pos(), node1.get_vel())].add((node2, weight))
        self.graph[(node2.get_pos(), node2.get_vel())].add((node1, weight)) # tou a partir do principio que é bidirecional



