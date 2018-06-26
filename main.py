import pygame.locals as locals
import copy

from MobObjects.MobCreator import *
from GameController import *
from ItemObjects.ItemCreator import *
from MapObject import *
from ConstantVariables import *


def set_window_settings(size, title):
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    return screen


def view_label(screen, point, text):
    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render(text, 1, (0, 0, 0))
    screen.blit(label, point)


def view_inventory_info(point, info):
    start_x = point[0]
    start_y = point[1]
    items = info['items']
    for index, item in items.items():
        if item['object'] is not None:
            view_label(game_screen, (start_x + 60 * index, start_y + 25), str(item['object'].get_name()))

            image = copy.copy(item['object'].get_image())
            rect = copy.copy(item['object'].rect)
            rect.x = start_x + 60 * index
            rect.y = start_y + 50
            game_screen.blit(image, rect)

            view_label(game_screen, (start_x + 30 + 60 * index, start_y + 55), str(item['amount']))

    view_label(game_screen, (start_x, start_y), 'inventory: ' + str(info['amount']))


def view_stats_info(point, info):
    start_x = point[0]
    start_y = point[1]
    counter = 0
    for index, stat in info.items():
        view_label(game_screen, (start_x, start_y + 25 * counter + 25), str(index) + ': ' + str(stat))
        counter += 1

    view_label(game_screen, (start_x, start_y), 'Stats: ')


closeWindow = False
pos = [0, 0]
win_coord = [0, 0]

game_screen = set_window_settings(screen_size, 'My PyGame Windows')

all_mobs = pygame.sprite.Group()
all_items = pygame.sprite.Group()
all_static = pygame.sprite.Group()
game_controller = GameController(game_screen, all_mobs, all_items, all_static)

game_map = MapObject('map_test', game_screen, game_controller, (50, 50), map_cell_size, 30, 15)
game_map.create_map_from_file('test_map.txt')

mob_creator = MobCreator(game_screen, game_map, game_controller)
item_creator = ItemCreator(game_screen, game_map, game_controller)

first_gob = mob_creator.create_goblin('first goblin', (1, 1), 5)
second_gob = mob_creator.create_goblin('second goblin', (19, 6), 3)
game_controller.add_mob(first_gob)
game_controller.add_mob(second_gob)

for i in range(3, 12):
    game_controller.add_item(item_creator.create_meat((i, 12)))

clock = pygame.time.Clock()
current_second = 0
while not closeWindow:
    focus = game_controller.get_focus()
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            closeWindow = True

        if event.type == locals.KEYDOWN:
            if focus:
                if isinstance(focus, MobObject):
                    if event.key == locals.K_w:
                        focus.go_up()
                    if event.key == locals.K_s:
                        focus.go_down()
                    if event.key == locals.K_a:
                        focus.go_left()
                    if event.key == locals.K_d:
                        focus.go_right()
                    if event.key == locals.K_p:
                        cell = game_map.get_cell(14, 5)
                        wall = cell.get_object()
                        cell.remove_object(wall)
                        game_controller.remove_static_object(wall)

        if event.type == locals.MOUSEBUTTONDOWN:
            if event.button == 1:
                win_coord = event.pos
                pos = game_map.get_cell_position_by_coord(event.pos[0], event.pos[1])
                cell = game_map.get_cell(pos[0], pos[1])
                game_controller.set_focus(cell.get_object())
            if event.button == 3:
                pos = game_map.get_cell_position_by_coord(event.pos[0], event.pos[1])
                if focus and isinstance(focus, MobObject):
                    focus.set_destination(pos[0], pos[1])

    second = int(pygame.time.get_ticks() / 1000)
    if current_second != second:
        current_second = second
        game_controller.update_mobs_condition()

    game_controller.update_mobs()

    game_map.draw_field(pygame.draw)

    game_controller.draw_static_objects()
    game_controller.draw_items()

    if focus:
        if isinstance(focus, MobObject):
            focus.draw_path(map_cell_size)

    game_controller.draw_mobs()

    if focus:
        if isinstance(focus, MobObject):
            view_label(game_screen, (150, 15), focus.get_name() + ' - ' + focus.get_action())

            view_label(game_screen, (25, 450),
                       'coords:      [' + str(int(focus.coord[0])) + ', ' + str(int(focus.coord[1])) + ']')

            view_label(game_screen, (25, 475),
                       'destination: [' +
                       str(int(focus.destination[0])) + ', ' +
                       str(int(focus.destination[1])) + ']'
                       )

            view_label(game_screen, (25, 500),
                       'vectors:     [' + str(int(focus.vectors[0])) + ', ' + str(int(focus.vectors[1])) + ']')

            view_label(game_screen, (25, 525),
                       'position:    [' + str(int(focus.rect.x)) + ', ' + str(int(focus.rect.y)) + ']')

            view_label(game_screen, (25, 550), 'path: ' + str(focus.path))

            view_inventory_info((25, 575), focus.get_inventory_info())

            view_stats_info((400, 450), focus.get_stats(['health', 'satiety']))

        else:
            view_label(game_screen, (200, 15), focus.get_name())
    else:
        view_label(game_screen, (200, 15), 'None')

    view_label(game_screen, (400, 5), 'x: ' + str(win_coord[0]) + '[' + str(pos[0]) + ']')
    view_label(game_screen, (400, 30), 'y: ' + str(win_coord[1]) + '[' + str(pos[1]) + ']')
    view_label(game_screen, (15, 15), str(current_second))

    pygame.display.update()

    clock.tick(fps)

pygame.quit()
quit()
