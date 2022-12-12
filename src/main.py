from parser import parser
from race import Race
from graph import Graph
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
        opt = 1  # int(input("Introduza a sua opção: "))

        match opt:
            case 1:
                path = "../circuits/circuito.txt"  # input("Indique a diretoria do ficheiro do circuito: ")
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
        print("6... Desenhar circuito")
        print("7... DFS")
        print("8... BFS")
        print("9... A*")
        print("10... Greedy")
        print("11... Voltar")
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
                race.graph.print_nodes()

            case 3:
                race.graph.print_edges()

            case 4:
                print()
                choice = menu_heuristic(race)
                race.graph.print_heuristics(choice)

            case 5:
                race.graph.draw()

            case 6:
                time=[1]
                for t in time:
                    drawer.create_frame(t, race.matrix)

                drawer.create_gif(time)
                drawer.print_gif()

            case 7:
                print()
                debug = menu_debug(race)
                (path, cost) = race.DFS_solution(debug)

                Graph.print_path(path)
                print(f"Custo: {cost}\n")

            case 8:
                print()
                path, cost, all_visited = race.BFS_solution()

                drawer.create_gif(race.matrix, all_visited)

                Graph.print_path(path)
                print(f"Custo: {cost}\n")

            case 9:
                print()
                choice = menu_heuristic(race)
                path, cost = race.a_star_solution(choice)
                race.print_result(path)

                Graph.print_path(path)
                print(f"Custo: {cost}\n")

            case 10:
                print()
                choice = menu_heuristic(race)
                path, cost = race.greedy_solution(choice)
                race.print_result(path)

                Graph.print_path(path)
                print(f"Custo: {cost}\n")

            case 11:
                print()
                main()
                break

            case other:
                print("\nOpção inválida!\n")


def main():
    race, multi_player = menu_build_graph()

    if race is not None:
        if multi_player is True:
            race.multiplayer()
        else:
            menu(race)


def menu_debug(race):
    opt = -1
    debug = False

    while opt not in {0, 1, 2}:
        print("=====================")
        print("Escolha de Modo")
        print("1... Debug")
        print("2... Normal")
        print("0... Voltar")
        print("=====================")

        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 0:
                print()
                menu(race)
                break
            case 1:
                debug = True
            case 2:
                break
            case other:
                print("\nOpção inválida!\n")

    return debug


def menu_heuristic(race):
    opt = -1
    choice = ""

    while opt not in {0, 1, 2}:
        print("=====================")
        print("Escolha de Heurística")
        print("1... Distância")
        print("2... Velocidade")
        print("0... Voltar")
        print("=====================")

        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 0:
                print()
                menu(race)
                break
            case 1:
                choice = "distance"
            case 2:
                choice = "velocity"
            case other:
                print("\nOpção inválida!\n")

    return choice


if __name__ == "__main__":
    main()
