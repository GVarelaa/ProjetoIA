from parser import parser
from race import Race
from graph import Graph
from node import Node


def menu_build_graph():
    race = None

    print("=========================")
    print("1... Construir grafo")
    print("0... Sair")
    print("=========================")

    opt = -1
    while opt != 0:
        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 1:
                path = input("Indique a diretoria do circuito: ")
                (matrix, start, end) = parser(path)[0]
                race = Race(matrix, start, end)
                race.build_graph(Node(3, 4, 0, 0, False, False, (0, 0)), [])
                print("\nCircuito carregado com sucesso!\n")
                break
            case 0:
                break

            case other:
                print("\nOpção inválida!\n")
                break

    return race


def menu(g):
    opt = -1
    while opt != 0:
        print("=========================")
        print("1... Imprimir grafo")
        print("2... Imprimir nodos")
        print("3... Imprimir arestas")
        print("4... Desenhar grafo")
        print("5... DFS")
        print("6... BFS")
        print("7... Voltar")
        print("0... Sair")
        print("=========================")

        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 0:
                break

            case 1:
                print(g)

            case 2:
                print(g.graph.keys())

            case 3:
                print(g.print_edges())

            case 4:
                g.draw()

            case 5:
                start = input("Nodo inicial: ")
                end = input("Nodo final: ")
                print(g.DFS(start, end, [], set()))

            case 6:
                start = input("Nodo inicial: ")
                end = input("Nodo final: ")
                print(g.BFS(start, end))

            case 7:
                main()
                break

            case other:
                print("\nOpção inválida!\n")


def main():
    race = menu_build_graph()

    if race is not None:
        g = race.graph
        menu(g)


if __name__ == "__main__":
    main()