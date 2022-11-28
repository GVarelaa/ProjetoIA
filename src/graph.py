import networkx as nx
import matplotlib.pyplot as plt

from queue import Queue

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

    def add_edge(self, node1, node2, cost):
        if node1 not in self.nodes:
            self.nodes.append(node1)
            self.graph[node1] = set()

        if node2 not in self.nodes:
            self.nodes.append(node2)
            self.graph[node2] = set()

        self.graph[node1].add((node2, cost))

    def get_arc_cost(self, node1, node2):
        total = 0

        adjs = self.graph[node1] #lista de arestas para aquele nodo
        for (node, cost) in adjs:
            if node == node2:
                total = cost

        return total

    def calc_path_cost(self, path):
        total = 0
        i = 0
        while i < len(path)-1:
             total += self.get_arc_cost(path[i], path[i+1])
             i += 1
        return total

    def DFS(self, start, end, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if start == end:
            total_cost = self.calc_path_cost(path)
            print()
            return (path, total_cost)

        for (adj, cost) in self.graph[start]:
            if adj not in visited:
                ret = self.DFS(adj, end, path, visited)
                if ret is not None:
                    return ret

        path.pop() #se nao encontrar, remover o que está no caminho
        return None

    def BFS(self, start, end):
        visited = set()
        q = Queue()

        q.put(start)
        visited.add(start)

        #garantir que o start node nao tem pais
        parents = dict()
        parents[start] = None

        path_found = False
        while not q.empty() and not path_found:
            node = q.get()

            if node == end:
                path_found = True
                print()
            else:
                for (adj, cost) in self.graph[node]:
                    if adj not in visited:
                        q.put(adj)
                        parents[adj] = node
                        visited.add(adj)

        #reconstruir o caminho
        path = []
        if path_found:
            path.append(end)
            while parents[end] is not None:
                path.append(parents[end])
                end = parents[end]
            path.reverse()

            total_cost = self.calc_path_cost(path)
            return (path, total_cost)

    def print_edges(self):
        l = ""
        for node in self.graph.keys():
            for (adj, cost) in self.graph[node]:
                l = l + str(node) + " -> " + str(adj) + " cost:" + str(cost) + "\n"
        return l

    def draw(self):
        verts = self.nodes
        g = nx.Graph()

        #Converter para o formato usado pela biblioteca networkx
        for node in verts:
            g.add_node(str(node))
            for (adj, cost) in self.graph[node]:
                l = (node, adj)
                g.add_edge(str(node), str(adj), cost=cost)

        #desenhar o grafo
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'cost')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()