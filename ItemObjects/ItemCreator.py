from ItemObjects.ItemObject import *
import random


class ItemCreator:
    screen = None
    map = None
    game_controller = None

    def __init__(self, screen, game_map, game_controller):
        self.screen = screen
        self.map = game_map
        self.game_controller = game_controller

    def create_meat(self, position):
        item = ItemObject('meat', self.screen, self.game_controller, self.map, position, (1, 1), 'Images/meat_alpha_1.1.png')
        item.set_edible(True)
        item.set_stat('satiety', 15)

        self.game_controller.add_item(item)
        return item

    def generate_items_around(self, point, radius=2, speed=2):
        if self.game_controller.get_time() % speed == 0:
            rand_x = random.randint((-1) * radius, radius)
            rand_y = random.randint((-1) * radius, radius)
            self.create_meat((point[0] + rand_x, point[1] + rand_y))

