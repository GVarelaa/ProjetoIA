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
    drawer.draw_paths(paths, race.matrix)