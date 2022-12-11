from parser import parser
from race import Race
from graph import Graph
from node import Node
import drawer

def menu_build_graph():
    race = None

    print("=========================")
    print("1... Construir grafo")
    print("0... Sair")
    print("=========================")

    opt = -1
    multi_player = False
    while opt != 0:
        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 1:
                path = input("Indique a diretoria do ficheiro do circuito: ")
                (matrix, start, end) = parser(path)
                race = Race(matrix, start, end)
                if len(start) == 1:
                    print("Um jogador")
                else:
                    print(str(len(start)) + " jogadores!")
                    multi_player = True
                race.build_graph()
                print("\nCircuito carregado com sucesso!\n")
                break
            case 0:
                break

            case other:
                print("\nOpção inválida!\n")
                break

    return race, multi_player


def menu(race):
    opt = -1
    while opt != 0:
        print("=========================")
        print("1... Imprimir grafo")
        print("2... Imprimir nodos")
        print("3... Imprimir arestas")
        print("4... Imprimir heurísticas")
        print("5... Desenhar grafo")
        print("6... DFS")
        print("7... BFS")
        print("8... A*")
        print("9... Greedy")
        print("10... Voltar")
        print("11... Desenhar circuito")
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
                print()
                print(race.graph.print_heuristics())

            case 5:
                race.graph.draw()

            case 6:
                choice = input("Modo debug? 1 - Sim, 0 - Não\n")
                if choice == '1':
                    debug = True
                else:
                    debug = False
                (path, cost) = race.DFS_solution(debug)
                print(Graph.print_path(path))
                print(f"Custo: {cost}\n")

            case 7:
                print()
                (path, cost) = race.BFS_solution()
                print(Graph.print_path(path))
                print(f"Custo: {cost}\n")

            case 8:
                choice = -1
                type = ""

                while choice != "distance" and choice != "velocity":
                    print("==== Heurística ====")
                    print("1 - Distância")
                    print("2 - Velocidade")
                    print("====================")

                    choice = int(input())

                    match choice:
                        case 1:
                            choice = "distance"
                        case 2:
                            choice = "velocity"
                        case other:
                            print("\nOpção inválida!\n")

                (path, cost) = race.a_star_solution(choice)
                print(Graph.print_path(path))
                print(f"Custo: {cost}\n")

            case 9:
                choice = -1
                type = ""

                while choice != "distance" and choice != "velocity":
                    print("==== Heurística ====")
                    print("1 - Distância")
                    print("2 - Velocidade")
                    print("====================")

                    choice = int(input())

                    match choice:
                        case 1:
                            choice = "distance"
                        case 2:
                            choice = "velocity"
                        case other:
                            print("\nOpção inválida!\n")

                (path, cost) = race.greedy_solution(choice)
                print(Graph.print_path(path))
                print(f"Custo: {cost}\n")

            case 10:
                print()
                main()
                break

            case 11:
                drawer.draw_circuit(race.matrix)
                break

            case other:
                print("\nOpção inválida!\n")


def main():
    race, multi_player  = menu_build_graph()

    if race is not None:
        if multi_player is True:
            race.multiplayer()
        else:
            menu(race)



if __name__ == "__main__":
    main()