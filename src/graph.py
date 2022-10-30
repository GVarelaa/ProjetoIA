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

    #def add_edge(self, node1, node2, weight):


