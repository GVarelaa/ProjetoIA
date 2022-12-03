import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
from queue import Queue
from node import Node
import time
from copy import deepcopy


def print_mat(mat):
    string = ""
    for l in mat:
        for c in l:
            string = string + str(c) + " "
        string += "\n"
    print(string)

class Graph:
    # construtor de classe
    def __init__(self):
        self.nodes = []  # lista com os nodos do grafo
        self.graph = {}  # dicionario do grafo
        self.h = {}  # dicionario com heuristicas

    def __str__(self):
        string = ""
        for key in self.graph.keys():
            string = string + str(key) + ": \n"

            for edge in self.graph[key]:
                string += "     " + str(edge) + "\n"

        return string

    def __repr__(self):
        string = ""
        for key in self.graph.keys():
            string = string + str(key) + ": \n"

            for edge in self.graph[key]:
                string += "     " + str(edge) + "\n"

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

    def add_heuristica(self, node, value):
        if node in self.nodes:
            self.h[node] = value

    def get_neighbours(self, node):
        lista = []
        for (adj, peso) in self.graph[node]:
            lista.append((adj, peso))
        return lista

    def get_arc_cost(self, node1, node2):
        total = 0

        adjs = self.graph[node1]  # lista de arestas para aquele nodo
        for (node, cost) in adjs:
            if node == node2:
                total = cost

        return total

    def calc_path_cost(self, path):
        total = 0
        i = 0

        while i < len(path) - 1:
            total += self.get_arc_cost(path[i], path[i + 1])
            i += 1

        return total
    @staticmethod
    def print_path(path):
        ret = ""

        for node in path:
            ret += str(node) + "\n"

        return ret

    def print_nodes(self):
        nodes = ""

        for node in self.nodes:
            nodes += str(node) + "\n"

        return nodes

    def print_edges(self):
        edges = ""

        for node in self.graph.keys():
            for (adj, cost) in self.graph[node]:
                edges += str(node) + "   ->   " + str(adj) + "    cost:" + str(cost) + "\n"

        return edges


    def print_heuristic(self):
        heuristic = ""

        for key in self.h.keys():
            heuristic += str(key) + " | " + str(self.h[key]) + "\n"

        return heuristic

    def count_edges(self):
        counter = 0
        for node in self.graph.keys():
            for (adj, cost) in self.graph[node]:
                counter += 1

        return counter

    def draw(self):
        verts = self.nodes
        g = nx.Graph()

        # Converter para o formato usado pela biblioteca networkx
        for node in verts:
            g.add_node(str(node))
            for (adj, cost) in self.graph[node]:
                l = (node, adj)
                g.add_edge(str(node), str(adj), cost=cost)

        # desenhar o grafo
        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'cost')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def DFS(self, start, end, matrix, debug, path=[], visited=set()):
        path.append(start)
        visited.add(start)

        if debug:
            print(start)

        for state in end:
            if state.pos == start.pos:
                total_cost = self.calc_path_cost(path)
                return path, total_cost

        for (adj, cost) in self.graph[start]:
            if adj not in visited:
                if debug:
                    print(adj.pos)
                    copy = deepcopy(matrix)
                    copy[len(matrix) - int(adj.pos[1]+0.5)][int(adj.pos[0]-0.5)] = 'O'
                    print_mat(copy)
                    input()
                ret = self.DFS(adj, end, matrix, debug, path, visited)
                if ret is not None:
                    return ret

        path.pop()  # se nao encontrar, remover o que está no caminho
        return None

    def BFS(self, start, end):
        visited = set()
        q = Queue()

        q.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais
        parents = dict()
        parents[start] = None

        path_found = False
        while not q.empty() and not path_found:
            node = q.get()

            for state in end:
                if node.pos == state.pos:
                    path_found = True

            if not path_found:
                for (adj, cost) in self.graph[node]:
                    if adj not in visited:
                        q.put(adj)
                        parents[adj] = node
                        visited.add(adj)

        # reconstruir o caminho
        path = []
        if path_found:
            path.append(node)
            while parents[node] is not None:
                path.append(parents[node])
                node = parents[node]
            path.reverse()

            total_cost = self.calc_path_cost(path)
            return path, total_cost

    def star(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos que ainda nao foram todos visitados(começa com start)
        # closed_list é uma lista de nodos visitados e todos os seus vizinhos já o foram
        custo_acumulado = dict()
        custo_acumulado[start] = 0

        open_list = set()
        close_list = set()

        open_list.add(start)

        parents = {}
        parents[start] = start

        i = 1

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n is None or (custo_acumulado[parents[v]] + self.get_arc_cost(v, parents[v]) + self.h[v]) < (
                        custo_acumulado[parents[n]] + self.get_arc_cost(n, parents[n]) + self.h[n]):
                    n = v

            # print(f"it {i} : {n}") # ver iteraçoes
            i += 1

            if n is None:
                print("Path doesnt exist")
                return None

            for state in end:
                if state.pos == n.pos:
                    reconst_path = []

                    while parents[n] != n:
                        reconst_path.append(n)
                        n = parents[n]

                    reconst_path.append(start)

                    reconst_path.reverse()

                    return (reconst_path, self.calc_path_cost(reconst_path))

            custo_acumulado[n] = custo_acumulado[parents[n]] + self.get_arc_cost(n, parents[n])

            for (m, weight) in self.get_neighbours(n):
                if m not in open_list and m not in close_list:
                    open_list.add(m)
                    parents[m] = n

            open_list.remove(n)
            close_list.add(n)

        print("Path doesnt exist")
        return None

    def greedy(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontraf nodo com a menor heuristica
            for v in open_list:
                if n is None or self.h[v] < self.h[n]:
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor


            for state in end:
                if state.pos == n.pos:
                    reconst_path = []

                    while parents[n] != n:
                        reconst_path.append(n)
                        n = parents[n]

                    reconst_path.append(start)

                    reconst_path.reverse()

                    return (reconst_path, self.calc_path_cost(reconst_path))

            # para todos os vizinhos  do nodo corrente
            for (m, weight) in self.get_neighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None


print_mat([[1,2,3],[1,2,3]])