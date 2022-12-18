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
        button2 = pygame.Rect(0, y // 7, x, 60)
        pygame.draw.rect(screen, (163, 163, 194), button2)
        draw_text("Escolha o circuito", font_titulo, "black", screen, x // 2, y // 5)

        button1 = pygame.Rect(SIZE_X - 100, SIZE_Y - 25, 200, 50)
        pygame.draw.rect(screen, (102, 153, 0), button1, border_radius=10)
        draw_text(circuits[index][0], font_pequena, "white", screen, x // 2, y // 2)

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
    while running:
        screen.fill("white")
        draw_text("Escolha o modo de jogo", font_titulo, "black", screen, x // 2, y // 5)

        mx, my = pygame.mouse.get_pos()

        button_sing = pygame.Rect(350, 200, 200, 50)
        button_mult = pygame.Rect(350, 300, 200, 50)
        text1 = font_titulo.render("Singleplayer", True, "white")
        text2 = font_titulo.render("Multiplayer", True, "white")

        if button_sing.collidepoint((mx, my)):
            if click:
                menus.menu_choose_algorithm(race)
                click = False

        if button_mult.collidepoint((mx, my)):
            if click:
                menu_multiplayer(race)
                click = False

        pygame.draw.rect(screen, (255, 0, 0), button_sing)
        pygame.draw.rect(screen, (255, 0, 0), button_mult)
        screen.blit(text1, (button_sing.x + 5, button_sing.y + 5))
        screen.blit(text2, (button_mult.x + 5, button_mult.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

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
    while running:
        screen.fill("white")
        draw_text("Escolha o algoritmo a utilizar", font_titulo, "black", screen, x // 2, y // 5)

        mx, my = pygame.mouse.get_pos()

        button_dfs = pygame.Rect(350, 200, 100, 30)
        button_bfs = pygame.Rect(350, 250, 100, 30)
        button_iterative = pygame.Rect(350, 300, 100, 30)
        button_uniform = pygame.Rect(350, 350, 100, 30)
        button_a_star = pygame.Rect(350, 400, 100, 30)
        button_greedy = pygame.Rect(350, 450, 100, 30)
        text_bfs = font_titulo.render("BFS", True, "white")
        text_dfs = font_titulo.render("DFS", True, "white")
        text_iterative = font_titulo.render("Iterative", True, "white")
        text_uniform = font_titulo.render("Uniform", True, "white")
        text_a_star = font_titulo.render("A*", True, "white")
        text_greedy = font_titulo.render("Greedy", True, "white")

        if button_bfs.collidepoint((mx, my)):
            if click:
                path, cost, pos_visited = race.BFS_solution(race.start[0])
                draw_paths([path], cost, race.matrix)

                click = False

        if button_dfs.collidepoint((mx, my)):
            if click:
                path, cost, pos_visited = race.DFS_solution(race.start[0])
                draw_paths([path], cost, race.matrix)

                click = False

        if button_iterative.collidepoint((mx, my)):
            if click:
                path, cost, pos_visited = race.iterative_DFS_solution(race.start[0])
                draw_paths([path], cost, race.matrix)

                click = False

        if button_uniform.collidepoint((mx, my)):
            if click:
                path, cost, pos_visited = race.uniform_cost_solution(race.start[0])
                draw_paths([path], cost, race.matrix)

                click = False

        if button_a_star.collidepoint((mx, my)):
            if click:
                path, cost, pos_visited = race.a_star_solution(race.start[0], "distance")
                draw_paths([path], cost, race.matrix)

                click = False

        if button_greedy.collidepoint((mx, my)):
            if click:
                path, cost, pos_visited = race.greedy_solution(race.start[0], "distance")
                draw_paths([path], cost, race.matrix)

                click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.draw.rect(screen, (255, 0, 0), button_bfs)
        pygame.draw.rect(screen, (255, 0, 0), button_dfs)
        pygame.draw.rect(screen, (255, 0, 0), button_iterative)
        pygame.draw.rect(screen, (255, 0, 0), button_uniform)
        pygame.draw.rect(screen, (255, 0, 0), button_a_star)
        pygame.draw.rect(screen, (255, 0, 0), button_greedy)
        screen.blit(text_bfs, (button_bfs.x + 5, button_bfs.y + 5))
        screen.blit(text_dfs, (button_dfs.x + 5, button_dfs.y + 5))
        screen.blit(text_iterative, (button_iterative.x + 5, button_iterative.y + 5))
        screen.blit(text_uniform, (button_uniform.x + 5, button_uniform.y + 5))
        screen.blit(text_a_star, (button_a_star.x + 5, button_a_star.y + 5))
        screen.blit(text_greedy, (button_greedy.x + 5, button_greedy.y + 5))

        pygame.display.update()
        clock.tick(60)


def draw_paths(paths, matrix, cost=-1):
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

    max_len = len(paths[0])
    for path in paths:
        if len(path) > max_len:
            max_len = len(path)

    i = 1
    while running:
        if i == max_len:
            break

        for path in paths:
            if i < len(path):
                start_pos = path[i-1].pos
                start_pos = (start_pos[0]*16, len(matrix)*16 - start_pos[1]*16)
                final_pos = path[i].pos
                final_pos = (final_pos[0]*16, len(matrix)*16 - final_pos[1]*16)
                pygame.draw.circle(screen, (153, 102, 0), start_pos, 5)
                pygame.draw.circle(screen, (153, 102, 0), final_pos, 5)
                pygame.draw.line(screen, (153, 102, 0), start_pos, final_pos, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.time.delay(500)
        pygame.display.update()
        i += 1

    click = False
    while running:
        mx, my = pygame.mouse.get_pos()

        button_back = pygame.Rect(400, 285, 100, 30)
        text = font_titulo.render("Voltar", True, "white")

        if button_back.collidepoint((mx, my)):
            if click:
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.draw.rect(screen, (255, 0, 0), button_back)
        screen.blit(text, (button_back.x + 5, button_back.y + 5))

        pygame.display.update()
        clock.tick(60)




circuits = list()
circuits.append(("Monaco", "../circuits/circuito3.txt"))
circuits.append(("Reta", "../circuits/circuito4.txt"))

main_menu(circuits)
