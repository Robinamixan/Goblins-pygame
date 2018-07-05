import math
import pygame
import json


class GameController:
    screen = None
    camera = None
    mobs_group = None
    items_group = None
    static_group = None
    focused = None
    current_second = 0

    def __init__(self, screen, camera, mobs_group, items_group, static_group):
        self.screen = screen
        self.camera = camera
        self.mobs_group = mobs_group
        self.items_group = items_group
        self.static_group = static_group
        open('rate.txt', 'w').close()

    #time
    def update_timer(self, second):
        self.current_second = second

    def get_time(self):
        return self.current_second

    def set_focus(self, game_object):
        self.focused = game_object

    def get_focus(self):
        return self.focused

    '''
        Static objects methods
    '''
    def add_static_object(self, static_object):
        self.static_group.add(static_object)

    def draw_static_objects(self):
        for sprite in self.static_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

    def remove_static_object(self, static_object):
        self.static_group.remove(static_object)

        cell = static_object.get_current_cell()
        cell.remove_object(static_object)

        static_object.kill()

    '''
        Mobs methods
    '''
    def add_mob(self, mob_object):
        self.mobs_group.add(mob_object)

    def draw_mobs(self):
        for sprite in self.mobs_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

    def remove_mob(self, mob_object):
        self.mobs_group.remove(mob_object)

        cell = mob_object.get_destination_cell()
        cell.remove_object(mob_object)

        self.save_mob_result(mob_object)

        mob_object.kill()
        if self.focused == mob_object:
            self.focused = None

    def update_mobs(self):
        self.mobs_group.update()

    def update_mobs_condition(self):
        for mob in self.mobs_group.sprites():
            mob.update_mob_condition()

    def save_mob_result(self, mob):
        with open('rate.txt', 'a') as file:
            time = pygame.time.get_ticks() / 1000

            json_string = json.dumps({'title': mob.title, 'time': str(time)})
            file.write(json_string + '\n')

    def save_mobs_result(self):
        for sprite in self.mobs_group:
            self.save_mob_result(sprite)
    '''
        Items methods
    '''
    def add_item(self, item_object):
        self.items_group.add(item_object)

    def draw_items(self):
        for sprite in self.items_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

    def remove_item(self, item_object):
        self.items_group.remove(item_object)

        cell = item_object.get_current_cell()
        cell.remove_object(item_object)

        item_object.kill()

    def get_items(self):
        return self.items_group.sprites()

    def get_nearest_item(self, point):
        length = 500
        nearest_item = None
        for item in self.get_items():
            coord = item.coord
            length_to_item = math.sqrt(math.pow(coord[0] - point[0], 2) + math.pow(coord[1] - point[1], 2))
            if length_to_item <= length:
                nearest_item = item
                length = length_to_item

        return nearest_item


