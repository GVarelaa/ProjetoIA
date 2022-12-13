import os
from parser import parser
from race import Race
from graph import Graph
import drawer


def menu_build_graph():
    race = None
    multiplayer = False

    print("=========================")
    print("1... Construir grafo")
    print("0... Sair")
    print("=========================")

    opt = 1
    match opt:

        case 0:
            exit()

        case 1:
            path = "../circuits/circuito.txt"  # input("Indique a diretoria do ficheiro do circuito: ")
            (matrix, start, end) = parser(path)
            race = Race(matrix, start, end)

            if len(start) == 1:
                print("Singleplayer ativo!")

            else:
                print("Multiplayer ativo com" + str(len(start)) + " jogadores!")
                multiplayer = True

            race.build_graph()
            print("\nCircuito carregado com sucesso!\n")

        case other:
            print("\nOpção inválida!\n")

    return race, multiplayer


def set_players_algorithms(race, opt):
    for state in race.start:
        race.player_algorithms[state] = opt


def menu_algorithms(race, multiplayer):
    opt = -1
    i = 0

    while opt not in {0, 1, 2, 3, 4} and i < len(race.start):
            opt = menu_algorithms_print(race, multiplayer, i)

            match opt:
                case 0:
                    print()
                    menu(race)
                    break
                case 1:
                    if multiplayer:
                        set_players_algorithms(race, opt)

                    print()
                    debug = menu_mode(race)
                    path, cost, all_visited = race.DFS_solution()

                    print()
                    Graph.print_path(path, cost)
                    drawer.draw_path(race.matrix, path)

                    if debug:
                        print("DEBUG MODE : A gerar GIF com iterações...\n")
                        drawer.create_gif(race.matrix, all_visited, "dfs_debug")

                case 2:
                    if multiplayer:
                        set_players_algorithms(race, opt)

                    print()
                    debug = menu_mode(race)
                    path, cost, all_visited = race.BFS_solution()

                    print()
                    Graph.print_path(path, cost)
                    drawer.draw_path(race.matrix, path)

                    if debug:
                        print("\nA gerar GIF com iterações...\n")
                        drawer.create_gif(race.matrix, all_visited, "bfs_debug")
                        print("GIF gerado com sucesso!\n")

                case 3:
                    if multiplayer:
                        set_players_algorithms(race, opt)

                    print()
                    debug = menu_mode(race)
                    print()
                    choice = menu_heuristic(race)
                    path, cost, all_visited = race.a_star_solution(choice)

                    print()
                    Graph.print_path(path, cost)
                    drawer.draw_path(race.matrix, path)

                    if debug:
                        print("\nA gerar GIF com iterações...\n")
                        drawer.create_gif(race.matrix, all_visited, "astar_debug")
                        print("GIF gerado com sucesso!\n")

                case 4:
                    if multiplayer:
                        set_players_algorithms(race, opt)

                    print()
                    debug = menu_mode(race)
                    print()
                    choice = menu_heuristic(race)
                    path, cost, all_visited = race.greedy_solution(choice)

                    print()
                    Graph.print_path(path, cost)
                    drawer.draw_path(race.matrix, path)

                    if debug:
                        print("\nA gerar GIF com iterações...\n")
                        drawer.create_gif(race.matrix, all_visited, "greedy_debug")
                        print("GIF gerado com sucesso!\n")

                case other:
                    print("\nOpção inválida!\n")

            i += 1


def menu_algorithms_print(race, multiplayer, i):
    print("=====================")
    if multiplayer:
        print(f"Escolha de Algoritmo (Jogador {i})")
    else:
        print("Escolha de Algoritmo")
    print("1.. DFS")
    print("2.. BFS")
    print("3.. A*")
    print("4.. Greedy")
    print("0.. Voltar")
    print("=====================")

    return int(input("Introduza a sua opção: "))


def menu_mode(race):
    opt = -1
    debug = False

    while opt not in {0, 1, 2}:
        print("=====================")
        print("Escolha de Modo")
        print("1... Normal")
        print("2... Debug")
        print("0... Voltar")
        print("=====================")

        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 0:
                print()
                menu(race)
                break
            case 1:
                break
            case 2:
                debug = True
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


def menu(race, multiplayer):
    opt = -1

    while opt != 0:
        print("==========================")
        print("1... Imprimir grafo")
        print("2... Imprimir nodos")
        print("3... Imprimir arestas")
        print("4... Imprimir heurísticas")
        print("5... Desenhar grafo")
        print("6... Desenhar circuito")
        print("7... Algoritmos de procura")
        print("8... Voltar")
        print("0... Sair")
        print("==========================")

        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 0:
                img_dir = "../img"
                for f in os.listdir(img_dir):
                    os.remove(os.path.join(img_dir, f))

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
                drawer.draw_path(race.matrix, [])

            case 7:
                print()
                menu_algorithms(race, multiplayer)

            case 8:
                print()
                main()
                break

            case other:
                print("\nOpção inválida!\n")


def main():
    race, multiplayer = menu_build_graph()

    if race is not None:
        if multiplayer:
            race.multiplayer()

        menu(race, multiplayer)


if __name__ == "__main__":
    main()
