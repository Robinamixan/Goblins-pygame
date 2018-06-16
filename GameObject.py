import pygame
from ConstantVariables import *


class GameObject(pygame.sprite.Sprite):
    title = ''
    window_position = []
    coord = [0, 0]
    width = 0
    height = 0
    screen = None
    map = None
    color = (0, 0, 0)

    def __init__(self, title, screen, game_map, position, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = pygame.Rect(position[0], position[1], size[0] * map_cell_size, size[1] * map_cell_size)

        self.title = title
        self.screen = screen
        self.map = game_map
        self.width = size[0]
        self.height = size[1]
        self.color = color

        self.coord = [position[0], position[1]]

    def update(self):
        return None

    def draw(self, cell_size):
        return None

    def get_name(self):
        return self.title

    def get_current_cell(self):
        return self.map.get_cell(self.coord[0], self.coord[1])


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
