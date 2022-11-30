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
                path = input("Indique a diretoria do ficheiro do circuito: ")
                (matrix, start, end) = parser(path)
                race = Race(matrix, start, end)
                race.build_graph()
                print("\nCircuito carregado com sucesso!\n")
                break
            case 0:
                break

            case other:
                print("\nOpção inválida!\n")
                break

    return race


def menu(race):
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
                print()
                print(race.graph)

            case 2:
                print()
                print(race.graph.print_nodes())

            case 3:
                print(race.graph.print_edges())

            case 4:
                race.graph.draw()

            case 5:
                print(race.DFS_solution())

            case 6:
                print(race.BFS_solution())

            case 7:
                print()
                main()
                break

            case other:
                print("\nOpção inválida!\n")


def main():
    race = menu_build_graph()

    if race is not None:
        menu(race)


if __name__ == "__main__":
    main()