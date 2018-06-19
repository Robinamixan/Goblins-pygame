from MobObjects.MobObject import *


class MobCreator:
    screen = None
    map = None

    def __init__(self, screen, game_map):
        self.screen = screen
        self.map = game_map

    def create_goblin(self, name, position, speed):
        return MobObject(name, self.screen, self.map, position, (1, 1), speed, 'Images/goblin_alpha_1.1.png')

