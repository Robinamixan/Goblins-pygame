import pygame

from GameObject import *
from ConstantVariables import *


class ItemObject(GameObject):
    def __init__(self, title, screen, game_map, position, size, image_path):
        super().__init__(title, screen, game_map, position, size, white)
        cell = self.get_current_cell()
        cell.set_object(self, True)

        self.rect.x = cell.x
        self.rect.y = cell.y

        self.image = pygame.image.load(image_path).convert_alpha()
