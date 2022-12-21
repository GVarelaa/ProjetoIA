import time
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
font_border = pygame.font.Font('freesansbold.ttf', 32)
clock = pygame.time.Clock()

input_rect = pygame.Rect(380, 200, 140, 32)

iman_img = pygame.image.load("../circuits/iman.png")
iman_img = pygame.transform.scale(iman_img, (300, 300))

bahrain_img = pygame.image.load("../circuits/bahrain.png")
bahrain_img = pygame.transform.scale(bahrain_img, (300, 300))

oval_img = pygame.image.load("../circuits/oval.png")
oval_img = pygame.transform.scale(oval_img, (300, 300))

vector_img = pygame.image.load("../circuits/vector.png")
vector_img = pygame.transform.scale(vector_img, (300, 300))

rect_img = pygame.image.load("../circuits/rect.png")
rect_img = pygame.transform.scale(rect_img, (400, 100))

#snake_img = pygame.image.load("../circuits/snake.png")
#snake_img = pygame.transform.scale(snake_img, (300,300))


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


def draw_shadow_text(screen, text, size, x, y, colour=(255,255,255), drop_colour=(77, 77, 77), font=None):
    # how much 'shadow distance' is best?
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.Font(font, size)
    # make the drop-shadow
    text_bitmap = text_font.render(text, True, drop_colour)
    text_rect = text_bitmap.get_rect()
    text_rect.center = (x+dropshadow_offset, y+dropshadow_offset)
    screen.blit(text_bitmap, text_rect)
    # make the overlay text
    text_bitmap = text_font.render(text, True, colour)
    text_rect = text_bitmap.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_bitmap, text_rect)


def main_menu(circuits):
    user_text = ""
    index = 0

    while True:
        screen.fill("white")
        draw_text("CIRCUITO", font_titulo, "black", screen, x // 2, y // 6)

        button = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 120, 225, 65)
        pygame.draw.rect(screen, (255, 204, 102), button, border_radius=15)
        pygame.draw.rect(screen, "black", button, width=2, border_radius=15)
        draw_shadow_text(screen, circuits[index][0], 30, x // 2, y // 2 - 87.5, font="freesansbold.ttf")

        draw_shadow_text(screen, ">", 50, x//2 + 135, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")
        draw_shadow_text(screen, "<", 50, x//2 - 140, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")

        if index == 0:
            screen.blit(iman_img, (SIZE_X - 150, 262.5))
        elif index == 1:
            screen.blit(bahrain_img, (SIZE_X - 150, 262.5))
        elif index == 2:
            screen.blit(oval_img, (SIZE_X - 150, 262.5))
        elif index == 3:
            screen.blit(vector_img, (SIZE_X - 150, 262.5))
        elif index == 4:
            screen.blit(rect_img, (SIZE_X - 200, 362.5))
        #elif index == 5:
            #screen.blit(snake_img), (SIZE_X - 200, 362.5)

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
    modes = ["Singleplayer", "Multiplayer"]
    while running:
        screen.fill("white")
        draw_text("MODO DE JOGO", font_titulo, "black", screen, x // 2, y // 5)

        button = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 120, 225, 65)
        pygame.draw.rect(screen, (255, 204, 102), button, border_radius=15)
        pygame.draw.rect(screen, "black", button, width=2, border_radius=15)
        draw_shadow_text(screen, modes[index], 30, x // 2, y // 2 - 87.5, font="freesansbold.ttf")

        draw_shadow_text(screen, ">", 50, x // 2 + 135, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")
        draw_shadow_text(screen, "<", 50, x // 2 - 140, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if index == 0:
                        menu_choose_algorithm(race)
                    else:
                        menu_multiplayer(race)

                elif event.key == pygame.K_LEFT:
                    index = loop_index_left(index, 2)

                elif event.key == pygame.K_RIGHT:
                    index = loop_index_right(index, 2)

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
        return "DFS Iterativo"
    elif integer == 3:
        return "Custo Uniforme"
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
    heuristics = ["distance", "velocity"]

    for i in range(len(players)):
        indexes[i] = (0, (0, 0))

    running = True
    index = 0
    vert_index = 0

    while running:
        screen.fill("white")
        draw_text("ALGORITMOS DE PROCURA", font_titulo, "black", screen, x//2, y//5)

        # Botão Player
        button_player = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 120, 225, 65)
        pygame.draw.rect(screen, (255, 204, 102), button_player, border_radius=15)
        draw_shadow_text(screen, f"Jogador {index}", 30, x//2, y//2 - 87.5, font="freesansbold.ttf")

        # Botão Algoritmo
        button_alg = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
        pygame.draw.rect(screen, (255, 179, 26), button_alg, border_radius=15)
        draw_shadow_text(screen, alg_handler(indexes[index][0]), 30, x//2, y//2)

        if vert_index == 0:
            pygame.draw.rect(screen, "black", button_player, width=2, border_radius=15)

            draw_shadow_text(screen, ">", 50, x // 2 + 135, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")
            draw_shadow_text(screen, "<", 50, x // 2 - 140, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")

        elif vert_index == 1:
            pygame.draw.rect(screen, (255, 179, 26), button_player, border_radius=15)
            draw_shadow_text(screen, f"Jogador {index}", 30, x // 2, y // 2 - 87.5, font="freesansbold.ttf")

            pygame.draw.rect(screen, (255, 204, 102), button_alg, border_radius=15)
            draw_shadow_text(screen, alg_handler(indexes[index][0]), 30, x // 2, y // 2)
            pygame.draw.rect(screen, "black", button_alg, width=2, border_radius=15)

            draw_shadow_text(screen, ">", 50, x // 2 + 135, y // 2 - 5.5, colour=(255, 179, 26), font="freesansbold.ttf")
            draw_shadow_text(screen, "<", 50, x // 2 - 140, y // 2 - 5.5, colour=(255, 179, 26), font="freesansbold.ttf")

            if indexes[index][0] == 4:
                button_heuristic = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 55, 225, 65)
                pygame.draw.rect(screen, (255, 179, 26), button_heuristic, border_radius=10)
                draw_shadow_text(screen, heur_handler(indexes[index][1][0]), 30, x // 2, SIZE_Y + 85, font="freesansbold.ttf")

            elif indexes[index][0] == 5:
                button_heuristic = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 55, 225, 65)
                pygame.draw.rect(screen, (255, 179, 26), button_heuristic, border_radius=10)
                draw_shadow_text(screen, heur_handler(indexes[index][1][1]), 30, x // 2, SIZE_Y + 85, font="freesansbold.ttf")

        elif vert_index == 2:
            pygame.draw.rect(screen, (255, 179, 26), button_player, border_radius=15)
            draw_shadow_text(screen, f"Jogador {index}", 30, x // 2, y // 2 - 87.5, font="freesansbold.ttf")

            pygame.draw.rect(screen, (255, 179, 26), button_alg, border_radius=15)
            draw_shadow_text(screen, alg_handler(indexes[index][0]), 30, x // 2, y // 2)

            button_heuristic = pygame.Rect(SIZE_X - 112.5, SIZE_Y + 55, 225, 65)
            pygame.draw.rect(screen, (255, 204, 102), button_heuristic, border_radius=10)
            pygame.draw.rect(screen, "black", button_heuristic, width=2, border_radius=10)

            draw_shadow_text(screen, ">", 50, x // 2 + 135, y // 2 + 80.5, colour=(255, 179, 26), font="freesansbold.ttf")
            draw_shadow_text(screen, "<", 50, x // 2 - 140, y // 2 + 80.5, colour=(255, 179, 26), font="freesansbold.ttf")

            if indexes[index][0] == 4:
                draw_shadow_text(screen, heur_handler(indexes[index][1][0]), 30, x // 2, SIZE_Y + 85, font="freesansbold.ttf")
            elif indexes[index][0] == 5:
                draw_shadow_text(screen, heur_handler(indexes[index][1][1]), 30, x // 2, SIZE_Y + 85, font="freesansbold.ttf")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if indexes[index][0] == 4 or indexes[index][0] == 5:
                        vert_index = loop_index_left(vert_index, 3)
                    else:
                        vert_index = loop_index_left(vert_index, 2)

                elif event.key == pygame.K_DOWN:
                    if indexes[index][0] == 4 or indexes[index][0] == 5:
                        vert_index = loop_index_right(vert_index, 3)
                    else:
                        vert_index = loop_index_left(vert_index, 2)

                elif event.key == pygame.K_LEFT:
                    if vert_index == 0:
                        index = loop_index_left(index, len(players))
                    elif vert_index == 1:
                        ind1, ind2 = indexes[index]
                        indexes[index] = (loop_index_left(indexes[index][0], 6), ind2)
                    elif vert_index == 2:
                        if indexes[index][0] == 4:
                            ind1, ind2 = indexes[index]
                            ind21, ind22 = ind2
                            ind21 = loop_index_left(ind21, 2)
                            indexes[index] = (ind1, (ind21, ind22))
                        elif indexes[index][0] == 5:
                            ind1, ind2 = indexes[index]
                            ind21, ind22 = ind2
                            ind22 = loop_index_left(ind22, 2)
                            indexes[index] = (ind1, (ind21, ind22))

                elif event.key == pygame.K_RIGHT:
                    if vert_index == 0:
                        index = loop_index_right(index, len(players))
                    elif vert_index == 1:
                        ind1, ind2 = indexes[index]
                        indexes[index] = (loop_index_right(indexes[index][0], 6), ind2)
                    elif vert_index == 2:
                        if indexes[index][0] == 4:
                            ind1, ind2 = indexes[index]
                            ind21, ind22 = ind2
                            ind21 = loop_index_right(ind21, 2)
                            indexes[index] = (ind1, (ind21, ind22))
                        elif indexes[index][0] == 5:
                            ind1, ind2 = indexes[index]
                            ind21, ind22 = ind2
                            ind22 = loop_index_right(ind22, 2)
                            indexes[index] = (ind1, (ind21, ind22))

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
        if race.player_algorithms[i] == 4:
            heuristics[i] = heur_handler(indexes[i][1][0])
        elif race.player_algorithms[i] == 5:
            heuristics[i] = heur_handler(indexes[i][1][1])

    paths, costs = race.multiplayer(heuristics)

    screen.fill("white")
    x_total = 450 - ((len(race.matrix[0]) // 2) * 16) - 16
    y_total = 300 - (len(race.matrix) // 2) * 16
    draw_circuit(race.matrix, x_total, y_total, 16)
    draw_paths(paths, race.matrix, costs)


def menu_choose_algorithm(race):
    running = True
    vert_index = 0
    index_alg = 0
    index_greedy = 0
    index_a = 0
    algorithms = ["BFS", "DFS", "DFS Iterativo", "Custo Uniforme", "A*", "Greedy"]
    heuristics = ["distance", "velocity"]

    while running:
        screen.fill("white")
        draw_text("ALGORITMO DE PROCURA", font_titulo, "black", screen, x // 2, y // 5)

        button_alg = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 120, 225, 65)

        if vert_index == 0:
            pygame.draw.rect(screen, (255, 204, 102), button_alg, border_radius=15)
            draw_shadow_text(screen, algorithms[index_alg], 20, x // 2, y // 2 - 87.5, font="freesansbold.ttf")
            pygame.draw.rect(screen, "black", button_alg, width=2, border_radius=15)

            draw_shadow_text(screen, ">", 50, x // 2 + 135, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")
            draw_shadow_text(screen, "<", 50, x // 2 - 140, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")

            if index_alg == 4:
                button_heuristic = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
                pygame.draw.rect(screen, (255, 179, 26), button_heuristic, border_radius=10)
                draw_shadow_text(screen, heuristics[index_a], 30, x // 2, y // 2, font="freesansbold.ttf")

            elif index_alg == 5:
                button_heuristic = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
                pygame.draw.rect(screen, (255, 179, 26), button_heuristic, border_radius=10)
                draw_shadow_text(screen, heuristics[index_greedy], 30, x // 2, y // 2, font="freesansbold.ttf")

        elif vert_index == 1:
            pygame.draw.rect(screen, (255, 179, 26), button_alg, border_radius=15)
            draw_shadow_text(screen, algorithms[index_alg], 20, x // 2, y // 2 - 87.5, font="freesansbold.ttf")

            button_heuristic = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 32.5, 225, 65)
            pygame.draw.rect(screen, (255, 204, 102), button_heuristic, border_radius=10)
            pygame.draw.rect(screen, "black", button_heuristic, width=2, border_radius=15)

            draw_shadow_text(screen, ">", 50, x // 2 + 135, y // 2 - 5.5, colour=(255, 179, 26), font="freesansbold.ttf")
            draw_shadow_text(screen, "<", 50, x // 2 - 140, y // 2 - 5.5, colour=(255, 179, 26), font="freesansbold.ttf")

            if index_alg == 4:
                draw_shadow_text(screen, heuristics[index_a], 30, x // 2, y // 2, font="freesansbold.ttf")
            elif index_alg == 5:
                draw_shadow_text(screen, heuristics[index_greedy], 30, x // 2, y // 2, font="freesansbold.ttf")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if vert_index == 0:
                        index_alg = loop_index_left(index_alg, 6)
                    else:
                        if index_alg == 4:
                            index_a = loop_index_left(index_a, 2)
                        elif index_alg == 5:
                            index_greedy = loop_index_left(index_greedy, 2)

                elif event.key == pygame.K_RIGHT:
                    if vert_index == 0:
                        index_alg = loop_index_right(index_alg, 6)
                    else:
                        if index_alg == 4:
                            index_a = loop_index_right(index_a, 2)
                        elif index_alg == 5:
                            index_greedy = loop_index_right(index_greedy, 2)

                elif event.key == pygame.K_DOWN:
                    if index_alg == 4 or index_alg == 5:
                        vert_index = loop_index_right(vert_index, 2)

                elif event.key == pygame.K_UP:
                    if index_alg == 4 or index_alg == 5:
                        vert_index = loop_index_left(vert_index, 2)

                elif event.key == pygame.K_RETURN:
                    player = menu_choose_player(race)
                    screen.fill("white")
                    x_total = 450 - ((len(race.matrix[0]) // 2) * 16) - 16
                    y_total = 300 - (len(race.matrix) // 2) * 16

                    if index_alg == 0:
                        path, cost, pos_visited = race.BFS_solution(player)
                        draw_circuit(race.matrix, x_total, y_total, 16)
                        draw_paths([path], race.matrix, [cost])

                    if index_alg == 1:
                        path, cost, pos_visited = race.DFS_solution(player)
                        draw_circuit(race.matrix, x_total, y_total, 16)
                        draw_paths([path], race.matrix, [cost])

                    if index_alg == 2:
                        path, cost, pos_visited = race.iterative_DFS_solution(player)
                        draw_circuit(race.matrix, x_total, y_total, 16)
                        draw_paths([path], race.matrix, [cost])

                    if index_alg == 3:
                        path, cost, pos_visited = race.uniform_cost_solution(player)
                        draw_circuit(race.matrix, x_total, y_total, 16)
                        draw_paths([path], race.matrix, [cost])

                    if index_alg == 4:
                        path, cost, pos_visited = race.a_star_solution(player, heuristics[index_a])
                        draw_circuit(race.matrix, x_total, y_total, 16)
                        draw_paths([path], race.matrix, [cost])

                    if index_alg == 5:
                        path, cost, pos_visited = race.greedy_solution(player, heuristics[index_greedy])
                        draw_circuit(race.matrix, x_total, y_total, 16)
                        draw_paths([path], race.matrix, [cost])

                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)


def menu_choose_player(race):
    running = True
    index = 0
    while running:
        screen.fill("white")
        draw_text("Jogador", font_titulo, "black", screen, x // 2, y // 5)

        # Botão Player
        button_player = pygame.Rect(SIZE_X - 112.5, SIZE_Y - 120, 225, 65)
        pygame.draw.rect(screen, (255, 204, 102), button_player, border_radius=15)
        draw_shadow_text(screen, f"Jogador {index}", 30, x // 2, y // 2 - 87.5, font="freesansbold.ttf")

        draw_shadow_text(screen, ">", 50, x // 2 + 135, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")
        draw_shadow_text(screen, "<", 50, x // 2 - 140, y // 2 - 90.5, colour=(255, 179, 26), font="freesansbold.ttf")

        draw_circuit(race.matrix, 450 - ((len(race.matrix[0]) // 2) * 10) - 10, 280, 10, index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    index = loop_index_left(index, len(race.start))
                elif event.key == pygame.K_RIGHT:
                    index = loop_index_right(index, len(race.start))
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)

    return race.start[index]


def draw_circuit(matrix, x_total, y_total, pixel, player=-1):
    # 900 * 600
    x_draw = x_total
    y_draw = y_total
    walls = list()
    finish = list()
    start = list()
    players = list()
    track = list()

    for row in matrix:
        for col in row:
            if col == "X":
                walls.append(pygame.Rect(x_draw, y_draw, pixel, pixel))
            elif col == "P":
                start.append(pygame.Rect(x_draw, y_draw, pixel, pixel))
                players.append((x_draw + (pixel//2) + 0.5, y_draw + (pixel//2) + 0.5))
            elif col == "F":
                finish.append(pygame.Rect(x_draw, y_draw, pixel, pixel))
            elif col == "-":
                track.append(pygame.Rect(x_draw, y_draw, pixel, pixel))
            x_draw += pixel
        y_draw += pixel
        x_draw = x_total

    for w in walls:
        pygame.draw.rect(screen, "white", w)

    for f in finish:
        pygame.draw.rect(screen, (255, 0, 0), f)
    for t in track:
        pygame.draw.rect(screen, (41, 41, 61), t)

    for s in start:
        pygame.draw.rect(screen, (51, 204, 51), s)

    if player != -1:
        pygame.draw.rect(screen, (255, 153, 0), start[player])


def draw_debug(pos_visited, matrix, x_total, y_total):
    for i in range(len(pos_visited)):
        curr_pos = pos_visited[i].pos
        curr_pos = (x_total + curr_pos[0] * 16, y_total + len(matrix) * 16 - curr_pos[1] * 16)
        if i > 0:
            pygame.draw.circle(screen, "black", curr_pos, 5)


def draw_final_path(path, matrix, x_total, y_total, cost, color):
    for i in range(len(path[1])):
        final_pos = path[1][i].pos
        final_pos = (x_total + final_pos[0] * 16, y_total + len(matrix) * 16 - final_pos[1] * 16)
        if i > 0:
            start_pos = path[1][i - 1].pos
            start_pos = (x_total + start_pos[0] * 16, y_total + len(matrix) * 16 - start_pos[1] * 16)
            pygame.draw.circle(screen, color, start_pos, 5)
            pygame.draw.line(screen, color, start_pos, final_pos, 2)
        pygame.draw.circle(screen, color, final_pos, 5)

    draw_text(f"J {path[0]} : Custo {cost}", font_pequena_pequena, color, screen, 80, 30 + 30*path[0])


def draw_until_frame(paths, matrix, x_total, y_total, index, costs):
    colors = ['darkviolet', 'darkorange', 'royalblue', 'turquoise', 'seagreen', 'pink', 'saddlebrown', 'palegreen','maroon']

    f_pos = None
    for j in range(len(paths)):
        if index + 1 < len(paths[j][1]):
            for i in range(index+1):
                final_pos = paths[j][1][i].pos
                f_pos = final_pos
                final_pos = (x_total + final_pos[0] * 16, y_total + len(matrix) * 16 - final_pos[1] * 16)
                if i > 0:
                    start_pos = paths[j][1][i - 1].pos
                    start_pos = (x_total + start_pos[0] * 16, y_total + len(matrix) * 16 - start_pos[1] * 16)
                    pygame.draw.circle(screen, colors[j], start_pos, 5)
                    pygame.draw.line(screen, colors[j], start_pos, final_pos, 2)

                pygame.draw.circle(screen, colors[j], final_pos, 5)
        else:
            draw_final_path(paths[j], matrix, x_total, y_total, costs[j], colors[j])


def draw_paths(paths, matrix, costs):
    x_total = 450 - ((len(matrix[0]) // 2) * 16) - 16
    y_total = 300 - (len(matrix) // 2) * 16
    max_len = len(paths[0][1])

    for path in paths:
        if len(path[1]) > max_len:
            max_len = len(path[1])

    i = 1
    index = 0
    running = True

    while running:
        time.sleep(0.15)
        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            index = loop_index_left(index, max_len)
            draw_circuit(matrix, x_total, y_total, 16)
            draw_until_frame(paths, matrix, x_total, y_total, index, costs)
        elif keys[K_RIGHT]:
            index = loop_index_right(index, max_len)
            draw_circuit(matrix, x_total, y_total, 16)
            draw_until_frame(paths, matrix, x_total, y_total, index, costs)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    index = loop_index_left(index, max_len)
                    draw_circuit(matrix, x_total, y_total, 16)
                    draw_until_frame(paths, matrix, x_total, y_total, index, costs)
                elif event.key == pygame.K_RIGHT:
                    index = loop_index_right(index, max_len)
                    draw_circuit(matrix,  x_total, y_total, 16)
                    draw_until_frame(paths, matrix, x_total, y_total, index, costs)
                elif event.key == pygame.K_ESCAPE:
                    running = False


        clock.tick(60)
        pygame.display.update()
        i += 1


circuits = list()
circuits.append(("Iman", "../circuits/iman.txt"))
circuits.append(("Bahrain", "../circuits/bahrain.txt"))
circuits.append(("Oval", "../circuits/oval.txt"))
circuits.append(("Vector", "../circuits/vector.txt"))
circuits.append(("Rect", "../circuits/rect.txt"))
circuits.append(("Snake", "../circuits/snake.txt"))
circuits.append(("Teste", "../circuits/test.txt"))
circuits.append(("Teste2", "../circuits/test2.txt"))

main_menu(circuits)
