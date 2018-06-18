import pygame

from pygame.locals import *
from MobObjects.MobObject import *
from MobObjects.MobCreator import *
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

game_map = MapObject('map_test', screen_game, (50, 50), map_cell_size, 30, 15)
game_map.create_map_from_file('test_map.txt')

mob_creator = MobCreator(screen_game, game_map)

all_mobs = pygame.sprite.Group()

first_gob = mob_creator.create_goblin('first goblin', (1, 1), 5)
second_gob = mob_creator.create_goblin('second goblin', (6, 7), 3)

all_mobs.add(first_gob)
all_mobs.add(second_gob)

myfont = pygame.font.SysFont("monospace", 15)

closeWindow = False
focused = None

clock = pygame.time.Clock()
pos = [0, 0]
win_coord = [0, 0]
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
                win_coord = event.pos
                pos = game_map.get_cell_position_by_coord(event.pos[0], event.pos[1])
                cell = game_map.get_cell(pos[0], pos[1])
                focused = cell.get_object()
            if event.button == 3:
                pos = game_map.get_cell_position_by_coord(event.pos[0], event.pos[1])
                if focused and isinstance(focused, MobObject):
                    focused.set_destination(pos[0], pos[1])

    all_mobs.update()

    game_map.draw_field(pygame.draw)
    game_map.draw_cells()

    if focused:
        if isinstance(focused, MobObject):
            focused.draw_path(map_cell_size)

    all_mobs.draw(screen_game)

    if focused:
        if isinstance(focused, MobObject):
            view_label(screen_game, (150, 25), focused.get_name() + ' - ' + focused.get_action())

            view_label(screen_game, (25, 450),
                       'coords:      [' + str(int(focused.coord[0])) + ', ' + str(int(focused.coord[1])) + ']')

            view_label(screen_game, (25, 475),
                       'destination: [' +
                       str(int(focused.destination[0])) + ', ' +
                       str(int(focused.destination[1])) + ']'
                       )

            view_label(screen_game, (25, 500),
                       'vectors:     [' + str(int(focused.vectors[0])) + ', ' + str(int(focused.vectors[1])) + ']')

            view_label(screen_game, (25, 525),
                       'position:    [' + str(int(focused.rect.x)) + ', ' + str(int(focused.rect.y)) + ']')

            view_label(screen_game, (25, 550), 'path: ' + str(focused.path))

        else:
            view_label(screen_game, (200, 25), focused.get_name())
    else:
        view_label(screen_game, (200, 25), 'None')

    view_label(screen_game, (400, 5), 'x: ' + str(win_coord[0]) + '[' + str(pos[0]) + ']')
    view_label(screen_game, (400, 30), 'y: ' + str(win_coord[1]) + '[' + str(pos[1]) + ']')

    pygame.display.update()

    clock.tick(fps)

pygame.quit()
quit()
