import pygame

from pygame.locals import *
from GameObject import *
from MapObject import *
from ConstantVariables import *


def set_window_settings(size, title):
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    return screen


screen_game = set_window_settings(screen_size, 'My PyGame Windows')

game_map = MapObject('map_test', screen_game, (50, 50), map_cell_size, 10, 15)
# TODO fix speed bug
first_rect = MobObject('first', screen_game, game_map, (1, 1), (1, 1), blue, 4)

game_map.create_wall([3, 4])

myfont = pygame.font.SysFont("monospace", 15)

closeWindow = False

clock = pygame.time.Clock()
pos = [0, 0]
while not closeWindow:
    for event in pygame.event.get():
        if event.type == QUIT:
            closeWindow = True

        if event.type == KEYDOWN:
            if event.key == K_w:
                first_rect.go_up()
            if event.key == K_s:
                first_rect.go_down()
            if event.key == K_a:
                first_rect.go_left()
            if event.key == K_d:
                first_rect.go_right()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = game_map.get_cell_by_coord(event.pos[0], event.pos[1])
            if event.button == 3:
                pos = game_map.get_cell_by_coord(event.pos[0], event.pos[1])
                first_rect.set_destination(pos[0], pos[1])

    game_map.update_cells()

    game_map.draw_field(pygame.draw)
    game_map.draw_cells()

    label1 = myfont.render(str(int(first_rect.destination[0])), 1, (0, 0, 0))
    label2 = myfont.render(str(int(first_rect.destination[1])), 1, (0, 0, 0))

    label3 = myfont.render(str(pos[0]), 1, (0, 0, 0))
    label4 = myfont.render(str(pos[1]), 1, (0, 0, 0))

    screen_game.blit(label1, (600, 100))
    screen_game.blit(label2, (600, 120))

    screen_game.blit(label3, (700, 100))
    screen_game.blit(label4, (700, 120))
    pygame.display.update()

    clock.tick(fps)

pygame.quit()
quit()
