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

    def get_image(self):
        return self.image

    def draw(self, cell_size):
        return None

    def get_name(self):
        return self.title

    def get_current_cell(self):
        return self.get_cell(self.coord[0], self.coord[1])

    def get_cell(self, x , y):
        return self.map.get_cell(x, y)

