import pygame

from pygame.locals import *
from MobObjects.MobObject import *
from MapObject import *
from ConstantVariables import *


def set_window_settings(size, title):
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    return screen


def view_label(screen, point, text):
    label = myfont.render(text, 1, (0, 0, 0))
    screen.blit(label, point)


screen_game = set_window_settings(screen_size, 'My PyGame Windows')

game_map = MapObject('map_test', screen_game, (50, 50), map_cell_size, 15, 15)

all_sprites = pygame.sprite.Group()
first_rect = MobObject('first', screen_game, game_map, (1, 1), (2, 2), blue, 5)

all_sprites.add(first_rect)

game_map.create_wall([3, 4])
game_map.create_wall([3, 5])

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
            if event.key == K_p:
                first_rect.stop()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = game_map.get_cell_by_coord(event.pos[0], event.pos[1])
            if event.button == 3:
                pos = game_map.get_cell_by_coord(event.pos[0], event.pos[1])
                first_rect.set_destination(pos[0], pos[1])

    # game_map.update_cells()
    all_sprites.update()

    game_map.draw_field(pygame.draw)
    game_map.draw_cells()

    all_sprites.draw(screen_game)

    view_label(screen_game, (600, 100), str(int(first_rect.destination[0])))
    view_label(screen_game, (600, 120), str(int(first_rect.destination[1])))

    view_label(screen_game, (600, 200), str(int(first_rect.coord[0])))
    view_label(screen_game, (600, 220), str(int(first_rect.coord[1])))

    view_label(screen_game, (600, 300), str(int(first_rect.vectors[0])))
    view_label(screen_game, (600, 320), str(int(first_rect.vectors[1])))
    view_label(screen_game, (450, 400), str(first_rect.path))

    view_label(screen_game, (500, 200), str(int(first_rect.window_position[0])))
    view_label(screen_game, (500, 220), str(int(first_rect.window_position[1])))

    view_label(screen_game, (700, 100), str(pos[0]))
    view_label(screen_game, (700, 120), str(pos[1]))

    pygame.display.update()

    clock.tick(fps)

pygame.quit()
quit()
