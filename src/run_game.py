import pygame
from pygame.locals import *
from race import Race
from parser import parser
import menus

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
        button1 = pygame.Rect(0, y // 7, x, 60)
        pygame.draw.rect(screen, (163, 163, 194), button1)
        draw_text("Escolha o circuito", font_titulo, "black", screen, x // 2, y // 5)

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
    click = False
    running = True
    index = 0
    while running:
        screen.fill("white")
        draw_text("Escolha o modo de jogo", font_titulo, "black", screen, x // 2, y // 5)

        mx, my = pygame.mouse.get_pos()

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


def menu_multiplayer(race):
    heuristics = dict()
    heuristics[0] = "distance"
    heuristics[1] = "distance"
    heuristics[2] = "distance"

    race.player_algorithms[0] = 4
    race.player_algorithms[1] = 4
    race.player_algorithms[2] = 4

    paths = race.multiplayer(heuristics)
    draw_paths(paths, race.matrix)


def menu_choose_algorithm(race):
    click = False
    running = True
    index = 0
    while running:
        screen.fill("white")
        draw_text("Escolha o algoritmo a utilizar", font_titulo, "black", screen, x // 2, y // 5)

        mx, my = pygame.mouse.get_pos()

        select1 = pygame.Rect(SIZE_X - 100, 175, 200, 40)
        select2 = pygame.Rect(SIZE_X - 100, 255, 200, 40)
        select3 = pygame.Rect(SIZE_X - 100, 325, 200, 40)
        select4 = pygame.Rect(SIZE_X - 100, 400, 200, 40)
        select5 = pygame.Rect(SIZE_X - 100, 475, 200, 40)
        select6 = pygame.Rect(SIZE_X - 100, 550, 200, 40)
        button_dfs = pygame.Rect(350, 175, 200, 40)
        button_bfs = pygame.Rect(350, 255, 200, 40)
        button_iterative = pygame.Rect(350, 325, 200, 40)
        button_uniform = pygame.Rect(350, 400, 200, 40)
        button_a_star = pygame.Rect(350, 475, 200, 40)
        button_greedy = pygame.Rect(350, 550, 200, 40)

        pygame.draw.rect(screen, (102, 153, 0), button_bfs, border_radius=15)
        pygame.draw.rect(screen, (102, 153, 0), button_dfs, border_radius=15)
        pygame.draw.rect(screen, (102, 153, 0), button_iterative, border_radius=15)
        pygame.draw.rect(screen, (102, 153, 0), button_uniform, border_radius=15)
        pygame.draw.rect(screen, (102, 153, 0), button_a_star, border_radius=15)
        pygame.draw.rect(screen, (102, 153, 0), button_greedy, border_radius=15)

        if index == 0:
            pygame.draw.rect(screen, (153, 204, 255), select1, width=5, border_radius=15)
        elif index == 1:
            pygame.draw.rect(screen, (153, 204, 255), select2, width=5, border_radius=15)
        elif index == 2:
            pygame.draw.rect(screen, (153, 204, 255), select3, width=5, border_radius=15)
        elif index == 3:
            pygame.draw.rect(screen, (153, 204, 255), select4, width=5, border_radius=15)
        elif index == 4:
            pygame.draw.rect(screen, (153, 204, 255), select5, width=5, border_radius=15)
        elif index == 5:
            pygame.draw.rect(screen, (153, 204, 255), select6, width=5, border_radius=15)

        draw_text("BFS", font_pequena, "white", screen, x // 2, 195)
        draw_text("DFS", font_pequena, "white", screen,  x // 2, 275)
        draw_text("Iterative", font_pequena, "white", screen,  x // 2, 345)
        draw_text("Uniform", font_pequena, "white", screen,  x // 2, 420)
        draw_text("A*", font_pequena, "white", screen,  x // 2, 495)
        draw_text("Greedy", font_pequena, "white", screen,  x // 2, 570)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    index = loop_index_left(index, 6)
                elif event.key == pygame.K_DOWN:
                    index = loop_index_right(index, 6)
                elif event.key == pygame.K_RETURN:
                    if index == 0:
                        path, cost, pos_visited = race.BFS_solution(race.start[0])
                        draw_paths([path], cost, race.matrix)

                    if index == 1:
                        path, cost, pos_visited = race.DFS_solution(race.start[0])
                        draw_paths([path], cost, race.matrix)

                    if index == 3:
                        path, cost, pos_visited = race.iterative_DFS_solution(race.start[0])
                        draw_paths([path], cost, race.matrix)

                    if index == 4:
                        path, cost, pos_visited = race.uniform_cost_solution(race.start[0])
                        draw_paths([path], cost, race.matrix)

                    if index == 5:
                        path, cost, pos_visited = race.a_star_solution(race.start[0], "distance")
                        draw_paths([path], cost, race.matrix)

                    if index == 6:
                        path, cost, pos_visited = race.greedy_solution(race.start[0], "distance")
                        draw_paths([path], cost, race.matrix)

                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)


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
circuits.append(("Reta", "../circuits/circuito4.txt"))
circuits.append(("Abu Dhabi", "../circuits/circuito1.txt"))

main_menu(circuits)
