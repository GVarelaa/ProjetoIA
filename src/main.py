import time
from parser import parser
from race import Race
from graph import Graph
import drawer


def menu_setup_race():
    race = None

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
            matrix, start, end = parser(path)
            race = Race(matrix, start, end)

            print("\nCircuito carregado com sucesso!\n")

        case other:
            print("\nOpção inválida!\n")

    return race


def set_players_algorithms(race, opt):
    for state in race.start:
        race.player_algorithms[state] = opt


def menu_choose_player(race):
    print("=========================================================")
    print("Qual dos jogadores pretende escolher como estado inicial:")

    i = 0
    players = []

    for player in race.start:
        players.append(i)
        print(f"Jogador {i} : ", end="")
        print(player)
        i += 1
    print("=========================================================")

    player = int(input("Introduza o número do jogador: "))

    if player not in players:
        print("\nO jogador introduzido não existe!\n")
        menu_choose_player(race)

    return race.start[player]


def menu_algorithms(race):
    opt = -1

    while opt not in {0, 1, 2, 3, 4}:
        print("=====================")
        print("Escolha de Algoritmo")
        print("1... DFS")
        print("2... BFS")
        print("3... Greedy")
        print("4... A*")
        print("0... Voltar")
        print("=====================")

        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 0:
                print()
                menu(race)
                break
            case 1:
                print()
                initial_state = menu_choose_player(race)

                print()
                debug = menu_mode(race)

                race.build_graph(initial_state=initial_state)
                path, cost, all_visited = race.DFS_solution(initial_state)

                print()
                Graph.print_path(path, cost)

                drawer.show_path_plot(race.matrix, path)

                if debug:
                    print("A gerar GIF com iterações...\n")
                    drawer.create_gif(race.matrix, all_visited, "dfs_debug")
                    print("GIF gerado com sucesso!\n")
                    time.sleep(1)

            case 2:
                print()
                initial_state = menu_choose_player(race)

                print()
                debug = menu_mode(race)

                race.build_graph(initial_state=initial_state)
                path, cost, all_visited = race.BFS_solution(initial_state)

                print()
                Graph.print_path(path, cost)

                drawer.show_path_plot(race.matrix, path)

                if debug:
                    print("A gerar GIF com iterações...\n")
                    drawer.create_gif(race.matrix, all_visited, "bfs_debug")
                    print("GIF gerado com sucesso!\n")
                    time.sleep(1)

            case 3:
                print()
                initial_state = menu_choose_player(race)

                print()
                debug = menu_mode(race)

                print()
                choice = menu_heuristic(race)

                race.build_graph(initial_state=initial_state)
                path, cost, all_visited = race.greedy_solution(initial_state, choice)

                print()
                Graph.print_path(path, cost)

                drawer.show_path_plot(race.matrix, path)

                if debug:
                    print("A gerar GIF com iterações...\n")
                    drawer.create_gif(race.matrix, all_visited, "greedy_debug")
                    print("GIF gerado com sucesso!\n")
                    time.sleep(1)

            case 4:
                print()
                initial_state = menu_choose_player(race)

                print()
                debug = menu_mode(race)

                print()
                choice = menu_heuristic(race)

                race.build_graph(initial_state=initial_state)
                path, cost, all_visited = race.a_star_solution(initial_state, choice)

                print()
                Graph.print_path(path, cost)

                drawer.show_path_plot(race.matrix, path)

                if debug:
                    print("A gerar GIF com iterações...\n")
                    drawer.create_gif(race.matrix, all_visited, "astar_debug")
                    print("GIF gerado com sucesso!\n")
                    time.sleep(1)

            case other:
                print("\nOpção inválida!\n")


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


def menu_multiplayer(race):
    print()
    print("======================================")
    print("Escolha dos algoritmos de cada jogador")

    i = 0
    for state in race.start:
        opt = -1
        while opt not in {1, 2, 3, 4}:
            print("=================================================================")
            print(f"Jogador {i}: ", end="")
            print(state)
            print("1... DFS")
            print("2... BFS")
            print("3... Greedy")
            print("4... A*")
            print("=================================================================")

            opt = int(input("Introduza a sua opção: "))
            if opt not in {1, 2, 3, 4}:
                print("\nOpção inválida!")

            print()

        race.player_algorithms[i] = opt

        i += 1


def menu(race):
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
        print("8... Multiplayer")
        print("9... Voltar")
        print("0... Sair")
        print("==========================")

        opt = int(input("Introduza a sua opção: "))

        match opt:
            case 0:
                drawer.clean_dir()

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
                drawer.show_circuit_plot(race.matrix)

            case 7:
                print()
                menu_algorithms(race)

            case 8:
                if len(race.start) < 2:
                    print("\nJogadores insuficientes para iniciar o modo multiplayer!\n")
                else:
                    menu_multiplayer(race)
                    race.multiplayer()

            case 9:
                print()
                main()
                break

            case other:
                print("\nOpção inválida!\n")


def main():
    race = menu_setup_race()
    menu(race)


if __name__ == "__main__":
    main()
