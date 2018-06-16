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
first_gob = MobObject('first goblin', screen_game, game_map, (1, 1), (1, 1), 5)

second_gob = MobObject('second goblin', screen_game, game_map, (6, 7), (1, 1), 3)

all_sprites.add(first_gob)
all_sprites.add(second_gob)

game_map.create_map_from_file('test_map.txt')

myfont = pygame.font.SysFont("monospace", 15)

closeWindow = False
focused = None

clock = pygame.time.Clock()
pos = [0, 0]
while not closeWindow:
    for event in pygame.event.get():
        if event.type == QUIT:
            closeWindow = True

        if event.type == KEYDOWN:
            if event.key == K_w:
                second_gob.go_up()
            if event.key == K_s:
                second_gob.go_down()
            if event.key == K_a:
                second_gob.go_left()
            if event.key == K_d:
                second_gob.go_right()
            if event.key == K_p:
                second_gob.stop()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = game_map.get_cell_position_by_coord(event.pos[0], event.pos[1])
                cell = game_map.get_cell(pos[0], pos[1])
                focused = cell.get_object()
            if event.button == 3:
                pos = game_map.get_cell_position_by_coord(event.pos[0], event.pos[1])
                if focused and isinstance(focused, MobObject):
                    focused.set_destination(pos[0], pos[1])

    # game_map.update_cells()
    all_sprites.update()

    game_map.draw_field(pygame.draw)
    game_map.draw_cells()

    if focused:
        if isinstance(focused, MobObject):
            focused.draw_path(map_cell_size)

    all_sprites.draw(screen_game)

    if focused:
        if isinstance(focused, MobObject):
            view_label(screen_game, (200, 25), focused.get_name() + ' - ' + focused.get_action())
        else:
            view_label(screen_game, (200, 25), focused.get_name())
    else:
        view_label(screen_game, (200, 25), 'None')

    view_label(screen_game, (600, 100), str(int(first_gob.destination[0])))
    view_label(screen_game, (600, 120), str(int(first_gob.destination[1])))

    view_label(screen_game, (600, 200), str(int(first_gob.coord[0])))
    view_label(screen_game, (600, 220), str(int(first_gob.coord[1])))

    view_label(screen_game, (600, 300), str(int(first_gob.vectors[0])))
    view_label(screen_game, (600, 320), str(int(first_gob.vectors[1])))
    view_label(screen_game, (450, 400), str(first_gob.path))

    view_label(screen_game, (500, 200), str(int(first_gob.rect.x)))
    view_label(screen_game, (500, 220), str(int(first_gob.rect.y)))

    view_label(screen_game, (700, 100), str(pos[0]))
    view_label(screen_game, (700, 120), str(pos[1]))

    pygame.display.update()

    clock.tick(fps)

pygame.quit()
quit()
