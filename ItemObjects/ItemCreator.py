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
        return ItemObject('meat_1', self.screen, self.game_controller, self.map, position, (1, 1), 'Images/meat_alpha_1.1.png')

    def create_meat_1(self, position):
        return ItemObject('meat_2', self.screen, self.game_controller, self.map, position, (1, 1), 'Images/meat_alpha_1.1.png')

    def create_meat_2(self, position):
        return ItemObject('meat_3', self.screen, self.game_controller, self.map, position, (1, 1), 'Images/meat_alpha_1.1.png')
