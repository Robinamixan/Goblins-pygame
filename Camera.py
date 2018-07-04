import pygame
from ConstantVariables import *


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def move_right(self, step):
        self.camera = pygame.Rect(self.camera.x + step, self.camera.y, self.width, self.height)

    def move_left(self, step):
        self.camera = pygame.Rect(self.camera.x - step, self.camera.y, self.width, self.height)

    def move_up(self, step):
        self.camera = pygame.Rect(self.camera.x, self.camera.y - step, self.width, self.height)

    def move_down(self, step):
        self.camera = pygame.Rect(self.camera.x, self.camera.y + step, self.width, self.height)

    def update(self, target):
        x = -target.rect.x + int(screen_size[0] / 2)
        y = -target.rect.y + int(screen_size[1] / 2)

        self.camera = pygame.Rect(x, y, self.width, self.height)
