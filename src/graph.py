import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue
from copy import deepcopy
import drawer
from src import position_calculator


def print_mat(mat):
    """
    Imprime a matriz
    :param mat: Matriz
    :return:
    """
    string = ""
    for l in mat:
        for c in l:
            string = string + str(c) + " "
        string += "\n"
    print(string)


class Graph:
    # construtor de classe
    def __init__(self):
        self.nodes = set()  # lista com os nodos do grafo
        self.graph = {}  # dicionario do grafo
        self.h1 = {}  # heurística da distância até a posição final
        self.h2 = {}  # heurística da velocidade

    def __str__(self):
        """

        :return:
        """
        string = ""
        for key in self.graph.keys():
            string = string + str(key) + ": \n"

            for edge in self.graph[key]:
                string += "     " + str(edge) + "\n"

        return string

    def __repr__(self):
        """

        :return:
        """
        string = ""
        for key in self.graph.keys():
            string = string + str(key) + ": \n"

            for edge in self.graph[key]:
                string += "     " + str(edge) + "\n"

        return string

    def get_node_by_pos(self, pos):
        """
        Obtem o nodo de uma posição
        :param pos: Posição
        :return: Nodo
        """
        for node in self.nodes:
            if node.get_pos() == pos:
                return node

    def add_edge(self, node1, node2, cost):
        """
        Adiciona uma aresta
        :param node1: Primeiro Nodo
        :param node2: Segundo Nodo
        :param cost: Custo
        :return:
        """
        if node1 not in self.nodes:
            self.nodes.add(node1)
            self.graph[node1] = set()

        if node2 not in self.nodes:
            self.nodes.add(node2)
            self.graph[node2] = set()

        self.graph[node1].add((node2, cost))

    def add_heuristic(self, node, value, type):
        """
        Adiciona uma heurística
        :param node: Nodo
        :param value: Valor
        :param type: Tipo
        :return:
        """
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        if node in self.nodes:
            heuristic[node] = value

    def get_neighbours(self, node):
        """
        Obtem a vizinhança de um nodo
        :param node: Nodo
        :return: Lista de nodos vizinhos
        """
        lista = []
        for (adj, peso) in self.graph[node]:
            lista.append((adj, peso))
        return lista

    def get_arc_cost(self, node1, node2):
        """
        Obtem o custo entre dois nodos
        :param node1: Primeiro Nodo
        :param node2: Segundo Nodo
        :return: Custo do arco
        """
        total = 0

        adjs = self.graph[node1]  # lista de arestas para aquele nodo
        for (node, cost) in adjs:
            if node == node2:
                total = cost

        return total

    def calc_path_cost(self, path):
        """
        Calcula o custo de um caminho
        :param path: Caminho
        :return: Custo do caminho
        """
        total = 0
        i = 0

        while i < len(path) - 1:
            total += self.get_arc_cost(path[i], path[i + 1])
            i += 1

        return total

    @staticmethod
    def print_path(path, cost):
        """
        Imprime o custo e os nodos de um caminho
        :param path: Caminho
        :param cost: Custo
        :return:
        """
        counter = 1
        res = ""

        for node in path:
            res += "Node " + str(counter) + " : " + str(node) + "\n"
            counter += 1

        print(res)
        print(f"Custo: {cost}\n")

    def print_nodes(self):
        """
        Imprime os nodos
        :return:
        """
        nodes = ""

        for node in self.nodes:
            nodes += str(node) + "\n"

        print(nodes)

    def print_edges(self):
        """
        Imrime as Arestas
        :return:
        """
        edges = ""

        for node in self.graph.keys():
            for (adj, cost) in self.graph[node]:
                edges += str(node) + "   ->   " + str(adj) + "    cost:" + str(cost) + "\n"

        print(edges)

    def print_heuristics(self, type):
        """
        Imprime as heurísticas
        :param type: tipo da heurística
        :return:
        """
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        heuristics = ""

        for key in heuristic.keys():
            heuristics += str(key) + " | " + str(heuristic[key]) + "\n"

        print(heuristics)

    def count_edges(self):
        """
        Conta o número de Arestas
        :return:
        """
        counter = 0
        for node in self.graph.keys():
            for (adj, cost) in self.graph[node]:
                counter += 1

        return counter

    def draw(self):
        """
        Desenha e imprime um Grafo
        :return:
        """
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

    @staticmethod
    def minor_length_path(paths):
        caminhos = list()

        for path in paths.values():
            caminhos.append(path)

        length = len(caminhos[0])
        for path in caminhos:
            if len(path) < length:
                length = len(path)

        return length

    @staticmethod
    def node_in_other_paths(start_node, final_node, iteration_number, paths):
        if len(paths.values()) < 1:
            return False

        disp = drawer.calculate_displacement(start_node.pos, final_node.pos)
        disp_squares = position_calculator.squares_visited(start_node.pos, disp)

        for list in paths.values():
            for square in disp_squares:
                if len(list) > iteration_number and list[iteration_number].pos == square:
                    return True
        return False

    def DFS(self, start, end, path, visited, pos_visited, paths=dict(), iter_number=0, depth=-1):
        """
        Algoritmo "Depth-First-Search"
        :param start: Posição inicial
        :param end: Posição final
        :param path: Caminho
        :param visited: Nodos Visitados
        :param pos_visited: Posições visitadas
        :param paths: Caminhos
        :param iter_number: Número de iterações
        :return:
        """
        path.append(start)
        visited.add(start)
        pos_visited.append(start.pos)  # debug

        for state in end:
            if state.pos == start.pos:
                total_cost = self.calc_path_cost(path)
                return path, total_cost, pos_visited

        if depth == 0:
            return None

        for adj, cost in self.graph[start]:
            if adj not in visited and not Graph.node_in_other_paths(state, adj, iter_number, paths):
                ret = self.DFS(adj, end, path, visited, pos_visited, paths, iter_number+1, depth-1)
                if ret is not None:
                    return ret

        path.pop()  # se nao encontrar, remover o que está no caminho
        return None

    def iterative_DFS(self, start, end, paths=dict()):
        i = 1
        path = []
        cost = 0
        path_found = False
        ret = None

        while ret is None:
            ret = self.DFS(start, end, path=[], visited=set(), pos_visited=[], paths=paths, depth=i)
            i += 1

        return ret

    def BFS(self, start, end, paths=dict()):
        """
        Algoritmo "Breadth-First-Search"
        :param start: Posição inicial
        :param end: Posição final
        :param paths: Caminhos
        :return: Caminho, Custo total e Posições visitadas
        """
        pos_visited = [start]  # debug
        visited = {start}
        q = Queue()
        i = 0

        q.put(start)

        # garantir que o start node nao tem pais
        parents = dict()
        parents[start] = None

        level = dict()
        level[start] = 0

        path_found = False
        while not q.empty() and not path_found:
            node = q.get()
            pos_visited.append(node.pos)  # debug

            for state in end:
                if node.pos == state.pos:
                    path_found = True

            if not path_found:
                for (adj, cost) in self.graph[node]:
                    i = level[node] + 1
                    if adj not in visited and not Graph.node_in_other_paths(state, adj, i, paths):
                        q.put(adj)
                        parents[adj] = node
                        level[adj] = i
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
            return path, total_cost, pos_visited

    def uniform_cost(self, start, end, paths=dict()):
        """
        Algoritmo Custo Uniforme
        :param start: Posição Inicial
        :param end: Posição Final
        :param paths: Caminhos
        :return:
        """
        level = {start: 0}

        open_list = {start}  # nodos visitados + vizinhos que ainda não foram todos visitados
        closed_list = set()  # nodos visitados
        parents = {start: start}  # mantém o antecessor de um nodo
        costs = {start: 0}

        pos_visited = [start.pos]  # debug

        while len(open_list) > 0:
            n = None

            # encontra nodo com a menor heuristica
            for node in open_list:
                if n is None or costs[node] < costs[n]:
                    n = node

            pos_visited.append(n.pos)  # debug

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start seguindo o antecessor
            for state in end:
                if state.pos == n.pos:
                    reconst_path = []

                    while parents[n] != n:
                        reconst_path.append(n)
                        n = parents[n]

                    reconst_path.append(start)
                    reconst_path.reverse()

                    return reconst_path, self.calc_path_cost(reconst_path), pos_visited

            for adj, cost in self.graph[n]:
                i = level[n] + 1
                if adj not in open_list and adj not in closed_list and not Graph.node_in_other_paths(n, adj, i, paths):
                    open_list.add(adj)
                    parents[adj] = n
                    level[adj] = i
                    costs[adj] = costs[n] + cost

            # remover n da open_list e adiciona-lo à closed_list - todos os seus vizinhos já foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        return None

    def greedy(self, start, end, type, paths=dict()):
        """
        Algoritmo Greedy
        :param start: Posição Inicial
        :param end: Posição Final
        :param type: Tipo
        :param paths: Caminhos
        :return:
        """
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        level = dict()
        level[start] = 0

        open_list = {start}  # nodos visitados + vizinhos que ainda não foram todos visitados
        closed_list = set()  # nodos visitados
        parents = {start: start}  # mantém o antecessor de um nodo

        pos_visited = [start.pos]  # debug

        while len(open_list) > 0:
            n = None

            # encontra nodo com a menor heuristica
            for node in open_list:
                if n is None or (heuristic[node] < heuristic[n]):
                    n = node

            pos_visited.append(n.pos)  # debug

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start seguindo o antecessor
            for state in end:
                if state.pos == n.pos:
                    reconst_path = []

                    while parents[n] != n:
                        reconst_path.append(n)
                        n = parents[n]

                    reconst_path.append(start)
                    reconst_path.reverse()

                    return reconst_path, self.calc_path_cost(reconst_path), pos_visited

            # para todos os vizinhos do nodo corrente
            for (adj, cost) in self.graph[n]:
                i = level[n] + 1
                if adj not in open_list and adj not in closed_list and not Graph.node_in_other_paths(n, adj, i, paths):
                    open_list.add(adj)
                    parents[adj] = n
                    level[adj] = i

            # remover n da open_list e adiciona-lo à closed_list - todos os seus vizinhos já foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        return None

    def a_star(self, start, end, type, paths=dict()):
        """
        Algoritmo "A-Star"
        :param start: Posição Inicial
        :param end: Posição Final
        :param type: Tipo
        :param paths: Caminhos
        :return:
        """
        if type == "distance":
            heuristic = self.h1
        elif type == "velocity":
            heuristic = self.h2

        level = {start: 0}

        open_list = {start}  # nodos visitados + vizinhos que ainda não foram todos visitados
        closed_list = set()  # nodos visitados
        parents = {start: start}  # mantém o antecessor de um nodo
        costs = {start: 0}

        pos_visited = [start.pos]  # debug

        while len(open_list) > 0:
            n = None

            # encontra nodo com a menor heuristica
            for node in open_list:
                if n is None or (heuristic[node] + costs[node]) < (heuristic[n] + costs[n]):
                    n = node

            pos_visited.append(n.pos)  # debug

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start seguindo o antecessor
            for state in end:
                if state.pos == n.pos:
                    reconst_path = []

                    while parents[n] != n:
                        reconst_path.append(n)
                        n = parents[n]

                    reconst_path.append(start)
                    reconst_path.reverse()

                    return reconst_path, self.calc_path_cost(reconst_path), pos_visited

            for adj, cost in self.graph[n]:
                i = level[n] + 1
                if adj not in open_list and adj not in closed_list and not Graph.node_in_other_paths(n, adj, i, paths):
                    open_list.add(adj)
                    parents[adj] = n
                    level[adj] = i
                    costs[adj] = costs[n] + cost

            # remover n da open_list e adiciona-lo à closed_list - todos os seus vizinhos já foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        return None
