import pygame

from GameObject import *
from ConstantVariables import *


class ItemObject(GameObject):
    edible = False
    satiety = 0

    def __init__(self, title, screen, game_controller, game_map, position, size, image_path):
        super().__init__(title, screen, game_controller, game_map, position, size, white)
        cell = self.get_current_cell()
        cell.set_object(self, self.passable)

        self.rect.x = cell.x
        self.rect.y = cell.y

        self.image = pygame.image.load(image_path).convert_alpha()

    def set_edible(self, edible):
        self.edible = edible

    def get_edible(self):
        return self.edible
