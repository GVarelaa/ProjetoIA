import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from copy import deepcopy
import drawer


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
        self.h1 = {}  # heurística da distância até a posição final
        self.h2 = {}  # heurística da velocidade

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

    def add_heuristic(self, node, value, type):
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        if node in self.nodes:
            heuristic[node] = value

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
    def print_path(path, cost):
        counter = 1
        res = ""

        for node in path:
            res += "Node " + str(counter) + " : " + str(node) + "\n"
            counter += 1

        print(res)
        print(f"Custo: {cost}\n")

    def print_nodes(self):
        nodes = ""

        for node in self.nodes:
            nodes += str(node) + "\n"

        print(nodes)

    def print_edges(self):
        edges = ""

        for node in self.graph.keys():
            for (adj, cost) in self.graph[node]:
                edges += str(node) + "   ->   " + str(adj) + "    cost:" + str(cost) + "\n"

        print(edges)

    def print_heuristics(self, type):
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        heuristics = ""

        for key in heuristic.keys():
            heuristics += str(key) + " | " + str(heuristic[key]) + "\n"

        print(heuristics)

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

    def DFS(self, start, end, path=[], visited=set(), all_visited=[]):
        path.append(start)
        visited.add(start)
        all_visited.append(start.pos)

        for state in end:
            if state.pos == start.pos:
                total_cost = self.calc_path_cost(path)
                return path, total_cost, all_visited

        for adj, cost in self.graph[start]:
            if adj not in visited:
                ret = self.DFS(adj, end, path, visited)
                if ret is not None:
                    return ret

        path.pop()  # se nao encontrar, remover o que está no caminho
        return None

    def BFS(self, start, end):
        all_visited = list()  #debug
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
            all_visited.append(node.pos)

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
            return path, total_cost, all_visited

    def a_star(self, start, end, type):
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        open_list = set()
        open_list.add(start)
        closed_list = set()
        parent = dict()
        parent[start] = start
        cost = dict()
        cost[start] = 0

        all_visited = [start.pos]

        while len(open_list) > 0:
            n1 = None
            for n2 in open_list:
                if (n1 is None) or (heuristic[n2] + cost[n2]) < (heuristic[n1] + cost[n1]):
                    n1 = n2

            all_visited.append(n1.pos)

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start seguindo o antecessor
            for state in end:
                if state.pos == n1.pos:
                    reconst_path = []

                    while parent[n1] != n1:
                        reconst_path.append(n1)
                        n1 = parent[n1]

                    reconst_path.append(start)

                    reconst_path.reverse()
                    return reconst_path, self.calc_path_cost(reconst_path), all_visited

            for adjacent, weight in self.graph[n1]:
                if adjacent not in open_list and adjacent not in closed_list:
                    open_list.add(adjacent)
                    parent[adjacent] = n1
                    cost[adjacent] = cost[n1] + weight

            open_list.remove(n1)
            closed_list.add(n1)

        return None

    def greedy(self, start, end, type):
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        open_list = set()
        open_list.add(start)
        closed_list = set()
        parent = dict()
        parent[start] = start
        all_visited = [start.pos]

        while len(open_list) > 0:
            n1 = None
            for n2 in open_list:
                if (n1 is None) or (heuristic[n2] < heuristic[n1]):
                    n1 = n2

            all_visited.append(n1.pos)

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start seguindo o antecessor
            for state in end:
                if state.pos == n1.pos:
                    reconst_path = []

                    while parent[n1] != n1:
                        reconst_path.append(n1)
                        n1 = parent[n1]

                    reconst_path.append(start)

                    reconst_path.reverse()

                    return reconst_path, self.calc_path_cost(reconst_path), all_visited

            # para todos os vizinhos  do nodo corrente
            for (adjacent, weight) in self.graph[n1]:
                if adjacent not in open_list and adjacent not in closed_list:
                    open_list.add(adjacent)
                    parent[adjacent] = n1

            open_list.remove(n1)
            closed_list.add(n1)

        return None
