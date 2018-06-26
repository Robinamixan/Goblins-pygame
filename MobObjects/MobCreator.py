from MobObjects.MobObject import *


class MobCreator:
    screen = None
    map = None
    game_controller = None

    def __init__(self, screen, game_map, game_controller):
        self.screen = screen
        self.map = game_map
        self.game_controller = game_controller

    def create_goblin(self, name, position, speed):
        gob = MobObject(name, self.screen, self.game_controller, self.map, position, (1, 1), speed, 'Images/goblin_alpha_1.1.png', 2)
        gob.set_stat('health', 150)
        gob.set_stat('satiety', 100)
        return gob

