from ItemObjects.ItemObject import *


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
        return item
