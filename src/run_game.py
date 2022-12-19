import pygame
from pygame.locals import *
from race import Race
from parser import parser
import menus
import sys

sys.setrecursionlimit(1000000)

pygame.init()
pygame.display.set_caption('Vector Race')

x = 900
y = 600

SIZE_X = 900 // 2
SIZE_Y = 600 // 2

screen = pygame.display.set_mode((x, y))
font_titulo = pygame.font.Font('freesansbold.ttf', 40)
font_pequena = pygame.font.Font('freesansbold.ttf', 30)
font_pequena_pequena = pygame.font.Font('freesansbold.ttf', 18)
clock = pygame.time.Clock()

input_rect = pygame.Rect(380, 200, 140, 32)

monaco_img = pygame.image.load("../circuits/monaco.png")
monaco_img = pygame.transform.scale(monaco_img, (200, 200))

bahrain_img = pygame.image.load("../circuits/bahrain.png")
bahrain_img = pygame.transform.scale(bahrain_img, (200, 200))

oval_img = pygame.image.load("../circuits/oval.png")
oval_img = pygame.transform.scale(oval_img, (200, 200))

vector_img = pygame.image.load("../circuits/vector.png")
vector_img = pygame.transform.scale(vector_img, (200, 200))

def loop_index_left(index, len):
    if index - 1 == -1:
        return len - 1
    else:
        return index - 1


def loop_index_right(index, len):
    if index + 1 == len:
        return 0
    else:
        return index+1


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def main_menu(circuits):
    user_text = ""
    index = 0

    while True:
        screen.fill("white")
        draw_text("CIRCUITO", font_titulo, "black", screen, x // 2, y // 5)

        button2 = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
        pygame.draw.rect(screen, (102, 153, 0), button2, border_radius=15)
        select = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
        pygame.draw.rect(screen, (153, 204, 255), select, width=5, border_radius=15)
        draw_text(circuits[index][0], font_pequena, "white", screen, x // 2, y // 2)

        button_left = pygame.Rect(SIZE_X - 112.5 - 200, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_left, border_radius=10)
        draw_text(circuits[loop_index_left(index, len(circuits))][0], font_pequena_pequena, "white", screen, SIZE_X - 112.5 - 125, y // 2)

        button_right = pygame.Rect(SIZE_X - 112.5 + 200 + 75, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_right, border_radius=10)
        draw_text(circuits[loop_index_right(index, len(circuits))][0], font_pequena_pequena, "white", screen, SIZE_X - 112.5 + 200 + 150, y // 2)

        if index == 0:
            screen.blit(monaco_img, (SIZE_X - 100, 350))
        elif index == 1:
            screen.blit(bahrain_img, (SIZE_X - 100, 350))
        elif index == 2:
            screen.blit(oval_img, (SIZE_X - 100, 350))
        elif index == 3:
            screen.blit(vector_img, (SIZE_X - 100, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    matrix, start, end = parser(circuits[index][1])
                    race = Race(matrix, start, end)
                    race.build_graph()

                    menu_choose_mode(race)
                elif event.key == pygame.K_LEFT:
                    index = loop_index_left(index, len(circuits))
                    circuit = circuits[index]
                elif event.key == pygame.K_RIGHT:
                    index = loop_index_right(index, len(circuits))
                    circuit = circuits[index]


        pygame.display.update()
        clock.tick(60)


def menu_choose_mode(race):
    running = True
    index = 0
    while running:
        screen.fill("white")
        draw_text("Escolha o modo de jogo", font_titulo, "black", screen, x // 2, y // 5)

        select1 = pygame.Rect(SIZE_X - 125, SIZE_Y - 55, 250, 50)
        select2 = pygame.Rect(SIZE_X - 125, SIZE_Y + 55, 250, 50)

        button_mult = pygame.Rect(SIZE_X - 125, SIZE_Y - 55, 250, 50)
        button_sing = pygame.Rect(SIZE_X - 125, SIZE_Y + 55, 250, 50)
        pygame.draw.rect(screen, (102, 153, 0), button_mult, border_radius=15)
        pygame.draw.rect(screen, (102, 153, 0), button_sing, border_radius=15)

        draw_text("Singleplayer", font_pequena, "white", screen, x // 2, SIZE_Y + 80)
        draw_text("Multiplayer", font_pequena, "white", screen, x // 2, SIZE_Y - 30)

        if index == 0:
            pygame.draw.rect(screen, (153, 204, 255), select1, width=5, border_radius=15)
        else:
            pygame.draw.rect(screen, (153, 204, 255), select2, width=5, border_radius=15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    index = loop_index_left(index, 2)
                elif event.key == pygame.K_DOWN:
                    index = loop_index_right(index, 2)
                elif event.key == pygame.K_RETURN:
                    if index == 0:
                        menu_multiplayer(race)
                    else:
                        menu_choose_algorithm(race)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)


def alg_handler(integer):
    if integer == 0:
        return "BFS"
    elif integer == 1:
        return "DFS"
    elif integer == 2:
        return "Iterativo"
    elif integer == 3:
        return "Uniforme"
    elif integer == 4:
        return "A*"
    elif integer == 5:
        return "Greedy"

def heur_handler(integer):
    if integer == 0:
        return "distance"
    elif integer == 1:
        return "velocity"

def menu_multiplayer_algorithms(players):
    indexes = dict()
    for i in range(len(players)):
        indexes[i] = (0, 0)

    running = True
    index = 0
    vertical_index = 0
    while running:
        screen.fill("white")
        draw_text("Escolha os algoritmos", font_titulo, "black", screen, x // 2, y // 5)

        button1 = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
        pygame.draw.rect(screen, (102, 153, 0), button1, border_radius=15)
        draw_text("Jogador " + str(index), font_pequena, "white", screen, x // 2, y // 2)

        button_left1 = pygame.Rect(SIZE_X - 112.5 - 200, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_left1, border_radius=10)
        draw_text("Jogador " + str(loop_index_left(index, len(players))), font_pequena_pequena, "white", screen, SIZE_X - 112.5 - 125,
                  y // 2)

        button_right1 = pygame.Rect(SIZE_X - 112.5 + 200 + 75, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_right1, border_radius=10)
        draw_text("Jogador " + str(loop_index_right(index, len(players))), font_pequena_pequena, "white", screen,
                  SIZE_X - 112.5 + 200 + 150, y // 2)

        button2 = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 70, 225, 65)
        pygame.draw.rect(screen, (102, 153, 0), button2, border_radius=15)
        draw_text(alg_handler(indexes[index][0]), font_pequena, "white", screen, x // 2, SIZE_Y + 100)

        button_left2 = pygame.Rect(SIZE_X - 112.5 - 200, SIZE_Y + 82.5, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_left2, border_radius=10)
        draw_text(alg_handler(loop_index_left(indexes[index][0], 6)), font_pequena_pequena, "white", screen,
                  SIZE_X - 112.5 - 125, SIZE_Y + 100)

        button_right2 = pygame.Rect(SIZE_X - 112.5 + 200 + 75, SIZE_Y + 82.5, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_right2, border_radius=10)
        draw_text(alg_handler(loop_index_right(indexes[index][0], 6)), font_pequena_pequena, "white", screen,
                  SIZE_X - 112.5 + 200 + 150, SIZE_Y + 100)

        if indexes[index][0] == 4 or indexes[index][0] == 5:
            button3 = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 172.5, 225, 65)
            pygame.draw.rect(screen, (102, 153, 0), button3, border_radius=15)
            draw_text(heur_handler(indexes[index][1]), font_pequena, "white", screen, x // 2, SIZE_Y + 200)

            button_left3 = pygame.Rect(SIZE_X - 112.5 - 200, SIZE_Y + 185, 150, 40)
            pygame.draw.rect(screen, (0, 153, 0), button_left3, border_radius=10)
            draw_text(heur_handler(loop_index_left(indexes[index][1], 2)), font_pequena_pequena, "white", screen,
                      SIZE_X - 112.5 - 125, SIZE_Y + 200)

            button_right3 = pygame.Rect(SIZE_X - 112.5 + 200 + 75, SIZE_Y + 185, 150, 40)
            pygame.draw.rect(screen, (0, 153, 0), button_right3, border_radius=10)
            draw_text(heur_handler(loop_index_right(indexes[index][1], 2)), font_pequena_pequena, "white", screen,
                      SIZE_X - 112.5 + 200 + 150, SIZE_Y + 200)

        if vertical_index == 0:
            select1 = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
            pygame.draw.rect(screen, (153, 204, 255), select1, width=5, border_radius=15)
        elif vertical_index == 1:
            select2 = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 70, 225, 65)
            pygame.draw.rect(screen, (153, 204, 255), select2, width=5, border_radius=15)
        elif vertical_index == 2:
            select3 = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 172.5, 225, 65)
            pygame.draw.rect(screen, (153, 204, 255), select3, width=5, border_radius=15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if indexes[index][0] == 4 or indexes[index][0] == 5:
                        vertical_index = loop_index_left(vertical_index, 3)
                    else:
                        vertical_index = loop_index_left(vertical_index, 2)
                elif event.key == pygame.K_DOWN:
                    if indexes[index][0] == 4 or indexes[index][0] == 5:
                        vertical_index = loop_index_right(vertical_index, 3)
                    else:
                        vertical_index = loop_index_left(vertical_index, 2)
                elif event.key == pygame.K_LEFT:
                    if vertical_index == 0:
                        index = loop_index_left(index, len(players))
                    elif vertical_index == 1:
                        ind1, ind2 = indexes[index]
                        indexes[index] = (loop_index_left(indexes[index][0], 6), ind2)
                    elif vertical_index == 2:
                        ind1, ind2 = indexes[index]
                        indexes[index] = (ind1, loop_index_left(indexes[index][1], 2))
                elif event.key == pygame.K_RIGHT:
                    if vertical_index == 0:
                        index = loop_index_right(index, len(players))
                    elif vertical_index == 1:
                        ind1, ind2 = indexes[index]
                        indexes[index] = (loop_index_right(indexes[index][0], 6), ind2)
                    elif vertical_index == 2:
                        ind1, ind2 = indexes[index]
                        indexes[index] = (ind1, loop_index_right(indexes[index][1], 2))
                elif event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)

    return indexes

def menu_multiplayer(race):
    heuristics = dict()

    indexes = menu_multiplayer_algorithms(race.start)

    for i in range(len(indexes.keys())):
        race.player_algorithms[i] = indexes[i][0]
        heuristics[i] = heur_handler(indexes[i][1])

    print(race.player_algorithms)
    print(heuristics)

    paths = race.multiplayer(heuristics)
    draw_paths(paths, race.matrix)



def menu_choose_algorithm(race):
    running = True
    index1 = 0
    index2 = 0
    index3 = 0
    algorithms = ["BFS", "DFS", "Iterativo", "Uniforme", "A*", "Greedy"]
    heuristics = ["distance", "velocity"]
    while running:
        screen.fill("white")
        draw_text("Escolha o algoritmo a utilizar", font_titulo, "black", screen, x // 2, y // 5)

        button = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
        pygame.draw.rect(screen, (102, 153, 0), button, border_radius=15)
        draw_text(algorithms[index1], font_pequena, "white", screen, x // 2, y // 2)

        button_left = pygame.Rect(SIZE_X - 112.5 - 200, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_left, border_radius=10)
        draw_text(algorithms[loop_index_left(index1, 6)], font_pequena_pequena, "white", screen, SIZE_X - 112.5 - 125, y // 2)

        button_right = pygame.Rect(SIZE_X - 112.5 + 200 + 75, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_right, border_radius=10)
        draw_text(algorithms[loop_index_right(index1, 6)], font_pequena_pequena, "white", screen, SIZE_X - 112.5 + 200 + 150, y // 2)

        if index1 == 4 or index1 == 5:
            button3 = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 70, 225, 65)
            pygame.draw.rect(screen, (102, 153, 0), button3, border_radius=15)
            draw_text(heuristics[index2], font_pequena, "white", screen, x // 2, SIZE_Y + 100)

            button_left3 = pygame.Rect(SIZE_X - 112.5 - 200, SIZE_Y + 82.5, 150, 40)
            pygame.draw.rect(screen, (0, 153, 0), button_left3, border_radius=10)
            draw_text(heuristics[loop_index_left(index2, 2)], font_pequena_pequena, "white", screen,
                      SIZE_X - 112.5 - 125, SIZE_Y + 100)

            button_right3 = pygame.Rect(SIZE_X - 112.5 + 200 + 75, SIZE_Y + 82.5, 150, 40)
            pygame.draw.rect(screen, (0, 153, 0), button_right3, border_radius=10)
            draw_text(heuristics[loop_index_left(index2, 2)], font_pequena_pequena, "white", screen,
                      SIZE_X - 112.5 + 200 + 150, SIZE_Y + 100)

        if index3 == 1:
            select2 = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 70, 225, 65)
            pygame.draw.rect(screen, (153, 204, 255), select2, width=5, border_radius=15)
        else:
            select1 = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
            pygame.draw.rect(screen, (153, 204, 255), select1, width=5, border_radius=15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if index3 == 0:
                        index1 = loop_index_left(index1, 6)
                    else:
                        index2 = loop_index_left(index2, 2)
                elif event.key == pygame.K_RIGHT:
                    if index3 == 0:
                        index1 = loop_index_right(index1, 6)
                    else:
                        index2 = loop_index_right(index2, 2)
                elif event.key == pygame.K_DOWN:
                    if index1 == 4 or index1 == 5:
                        index3 = loop_index_right(index3, 2)
                elif event.key == pygame.K_UP:
                    if index1 == 4 or index1 == 5:
                        index3 = loop_index_left(index3, 2)
                elif event.key == pygame.K_RETURN:
                    player = menu_choose_player(race.start)
                    if index1 == 0:
                        print("BFS")
                        path, cost, pos_visited = race.BFS_solution(player)
                        draw_paths([path], race.matrix, cost)

                    if index1 == 1:
                        print("DFS")
                        path, cost, pos_visited = race.DFS_solution(player)
                        draw_paths([path], race.matrix, cost)

                    if index1 == 2:
                        print("Iterativo")
                        path, cost, pos_visited = race.iterative_DFS_solution(player)
                        draw_paths([path], race.matrix, cost)

                    if index1 == 3:
                        print("Uniforme")
                        path, cost, pos_visited = race.uniform_cost_solution(player)
                        draw_paths([path], race.matrix, cost)

                    if index1 == 4:
                        print("A*")
                        print(heuristics[index2])
                        path, cost, pos_visited = race.a_star_solution(player, heuristics[index2])
                        draw_paths([path], race.matrix, cost)

                    if index1 == 5:
                        print("Greedy")
                        print(heuristics[index2])
                        path, cost, pos_visited = race.greedy_solution(player, heuristics[index2])
                        draw_paths([path], race.matrix, cost)

                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)

def menu_choose_player(players):
    running = True
    index = 0
    while running:
        screen.fill("white")
        draw_text("Escolha o jogador", font_titulo, "black", screen, x // 2, y // 5)

        button = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
        pygame.draw.rect(screen, (102, 153, 0), button, border_radius=15)
        draw_text("Jogador " + str(index), font_pequena, "white", screen, x // 2, y // 2)
        draw_text(str(players[index].pos), font_pequena, "black", screen, x // 2, y // 2 + 100)

        button_left = pygame.Rect(SIZE_X - 112.5 - 200, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_left, border_radius=10)
        draw_text("Jogador " + str(loop_index_left(index, len(players))), font_pequena_pequena, "white", screen, SIZE_X - 112.5 - 125,
                  y // 2)

        button_right = pygame.Rect(SIZE_X - 112.5 + 200 + 75, SIZE_Y - 20, 150, 40)
        pygame.draw.rect(screen, (0, 153, 0), button_right, border_radius=10)
        draw_text("Jogador " + str(loop_index_right(index, len(players))), font_pequena_pequena, "white", screen,
                  SIZE_X - 112.5 + 200 + 150, y // 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    index = loop_index_left(index, len(players))
                elif event.key == pygame.K_RIGHT:
                    index = loop_index_right(index, len(players))
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)

    return players[index]


def draw_circuit(matrix):
    x_draw = y_draw = 0
    walls = list()
    finish = list()
    start = list()
    players = list()
    track = list()

    for row in matrix:
        for col in row:
            if col == "X":
                walls.append(pygame.Rect(x_draw, y_draw, 16, 16))
            elif col == "P":
                start.append(pygame.Rect(x_draw, y_draw, 16, 16))
                players.append((x_draw + 8.5, y_draw + 8.5))
            elif col == "F":
                finish.append(pygame.Rect(x_draw, y_draw, 16, 16))
            elif col == "-":
                track.append(pygame.Rect(x_draw, y_draw, 16, 16))
            x_draw += 16
        y_draw += 16
        x_draw = 0

    running = True

    screen.fill("white")

    for w in walls:
        pygame.draw.rect(screen, "white", w)
    for f in finish:
        pygame.draw.rect(screen, (255, 0, 0), f)
    for t in track:
        pygame.draw.rect(screen, (41, 41, 61), t)
    for s in start:
        pygame.draw.rect(screen, (51, 204, 51), s)


def draw_until_frame(paths, matrix, index):
    colors = ["orange", "red", "green", "blue", "yellow", "magenta", "gray", "cyan"]
    for j in range(len(paths)):
        if index < len(paths[j]):
            for i in range(index+1):
                final_pos = paths[j][i].pos
                final_pos = (final_pos[0] * 16, len(matrix) * 16 - final_pos[1] * 16)
                if i > 0:
                    start_pos = paths[j][i - 1].pos
                    start_pos = (start_pos[0] * 16, len(matrix) * 16 - start_pos[1] * 16)
                    pygame.draw.circle(screen, colors[j], start_pos, 5)
                    pygame.draw.line(screen, colors[j], start_pos, final_pos, 2)

                pygame.draw.circle(screen, colors[j], final_pos, 5)


def draw_frame(paths, matrix, index):
    for path in paths:
        if index < len(path):
            final_pos = path[index].pos
            final_pos = (final_pos[0] * 16, len(matrix) * 16 - final_pos[1] * 16)
            if index > 0:
                start_pos = path[index - 1].pos
                start_pos = (start_pos[0] * 16, len(matrix) * 16 - start_pos[1] * 16)
                pygame.draw.circle(screen, (153, 102, 0), start_pos, 5)
                pygame.draw.line(screen, (153, 102, 0), start_pos, final_pos, 2)

            pygame.draw.circle(screen, (153, 102, 0), final_pos, 5)


def draw_paths(paths, matrix, cost=-1):
    draw_circuit(matrix)

    max_len = len(paths[0])
    for path in paths:
        if len(path) > max_len:
            max_len = len(path)

    i = 1
    index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    index = loop_index_left(index, max_len)
                    draw_circuit(matrix)
                    draw_until_frame(paths, matrix, index)
                elif event.key == pygame.K_RIGHT:
                    index = loop_index_right(index, max_len)
                    draw_circuit(matrix)
                    draw_until_frame(paths, matrix, index)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(60)
        pygame.display.update()
        i += 1



circuits = list()
circuits.append(("Monaco", "../circuits/circuito3.txt"))
circuits.append(("Bahrain", "../circuits/bahrain_simp.txt"))
circuits.append(("Oval", "../circuits/oval.txt"))
circuits.append(("Vector", "../circuits/vector.txt"))

main_menu(circuits)
