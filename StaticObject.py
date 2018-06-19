import pygame

from GameObject import *
from ConstantVariables import *


class StaticObject(GameObject):
    def __init__(self, title, screen, game_map, position, size, color):
        super().__init__(title, screen, game_map, position, size, color)
        self.image = pygame.Surface((size[0] * map_cell_size, size[1] * map_cell_size))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        cell = self.get_current_cell()
        cell.set_object(self, False)

        self.rect.x = cell.x
        self.rect.y = cell.y
