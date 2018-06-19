from ItemObjects.ItemObject import *


class ItemCreator:
    screen = None
    map = None

    def __init__(self, screen, game_map):
        self.screen = screen
        self.map = game_map

    def create_meat(self, name, position):
        return ItemObject(name, self.screen, self.map, position, (1, 1), 'Images/meat_alpha_1.1.png')

