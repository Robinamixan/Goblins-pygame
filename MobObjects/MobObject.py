import math
import copy
from main import remove_object_from_map

from GameObject import *
from InventoryObjects.InventoryObject import *
from ConstantVariables import *


class MobObject(GameObject):
    speed = 1
    vectors = [0, 0]
    destination = []
    path = []
    action = 'w'
    stock = None
    inventory = None

    def __init__(self, title, screen, game_map, position, size, speed=1, image_path='', inventory_size=0):
        super().__init__(title, screen, game_map, position, size, white)
        self.speed = speed

        cell = self.get_current_cell()
        cell.set_object(self, False)

        self.rect.x = cell.x
        self.rect.y = cell.y

        self.image = pygame.image.load(image_path).convert_alpha()

        self.destination = [position[0], position[1]]

        self.inventory = InventoryObject(inventory_size)

    # Getting current acts of mob
    def get_action(self):
        action_string = ''

        if self.action == 'wait':
            action_string = 'waiting'

        if self.action == 'wait_clear':
            action_string = 'waiting clear path'

        if self.action == 'move':
            action_string = 'going'

        if self.action == 'get':
            action_string = 'getting'

        return action_string

    # Get destination cell by current destination coord
    def get_destination_cell(self):
        return self.get_cell(self.destination[0], self.destination[1])

    # Set destination coord on the map and change action to 'move'
    def set_destination(self, row, column):
        self.create_path([self.destination[0], self.destination[1]], [row, column])
        if row and column:
            cell = self.get_cell(row, column)
            if cell.is_empty():
                self.action = 'move'
            else:
                self.action = 'get'

    # Creating move path by start and end points
    def create_path(self, start, end):
        path = []
        current_step = [0, 0]

        step_number = 0

        (current_step[0], current_step[1]) = (start[0], start[1])

        if self.path:
            step_number += 1
            path.append([current_step[0], current_step[1]])

        while end != current_step:
            path.append([current_step[0], current_step[1]])
            if current_step[0] < end[0]:
                current_step[0] += 1
                path[step_number][0] = current_step[0]

            if current_step[0] > end[0]:
                current_step[0] -= 1
                path[step_number][0] = current_step[0]

            if current_step[1] < end[1]:
                current_step[1] += 1
                path[step_number][1] = current_step[1]

            if current_step[1] > end[1]:
                current_step[1] -= 1
                path[step_number][1] = current_step[1]

            step_number += 1

        self.path = path

    # Movement commands
    def go_left(self):
        self.set_destination(self.destination[0] - 1, self.destination[1])

    def go_right(self):
        self.set_destination(self.destination[0] + 1, self.destination[1])

    def go_up(self):
        self.set_destination(self.destination[0], self.destination[1] - 1)

    def go_down(self):
        self.set_destination(self.destination[0], self.destination[1] + 1)

    # Stops mob on his current cell
    def stop(self):
        cell = self.get_destination_cell()
        (self.rect.x, self.rect.y) = (cell.x, cell.y)
        self.coord = [self.destination[0], self.destination[1]]
        self.vectors[0] = 0
        self.vectors[1] = 0
        if self.path:
            self.action = 'wait_clear'
        elif self.action == 'get':
            items = copy.copy(cell.contain)
            items.pop(-1)
            for item in items:
                self.catch_item(item)
                cell.remove_object(item)
                remove_object_from_map(item)
            self.action = 'wait'
        else:
            self.action = 'wait'

    def update(self):
        if self.path:
            if self.destination == self.coord:
                self.go_to_next_step()
            else:
                self.update_move()
        else:
            self.stop()

    def go_to_next_step(self):
        next_step = self.path[0]
        if next_step == self.coord:
            self.path.pop(0)
            next_step = self.path[0]
        next_cell = self.get_cell(next_step[0], next_step[1])
        if next_cell.is_can_move(self):
            current_cell = self.get_cell(self.coord[0], self.coord[1])
            current_cell.remove_object(self)
            next_cell.set_object(self)
            self.destination = next_step
            self.update_move()
        else:
            self.stop()

    def update_move(self):
        cell = self.get_destination_cell()
        if self.is_destination_x(cell) and self.is_destination_y(cell):
            self.coord = [self.destination[0], self.destination[1]]
            self.path.pop(0)
            self.update_vectors_in_wait_position()
        else:
            if self.is_destination_x(cell):
                self.rect.x = cell.x
                self.coord[0] = self.destination[0]

            if self.is_destination_y(cell):
                self.rect.y = cell.y
                self.coord[1] = self.destination[1]

            self.update_vectors(cell)
            self.set_next_position()

    def update_vectors(self, cell):
        if self.rect.x > cell.x:
            self.vectors[0] = -1
        else:
            if self.rect.x < cell.x:
                self.vectors[0] = 1
            else:
                self.vectors[0] = 0

        if self.rect.y > cell.y:
            self.vectors[1] = -1
        else:
            if self.rect.y < cell.y:
                self.vectors[1] = 1
            else:
                self.vectors[1] = 0

        if self.vectors[0] == 0 and self.vectors[1] == 0:
            self.update_vectors_in_wait_position()

    def update_vectors_in_wait_position(self):
        if self.path:
            next_destin = self.path[0]

            if next_destin[0] > self.coord[0]:
                self.vectors[0] = 1
            else:
                if next_destin[0] < self.coord[0]:
                    self.vectors[0] = -1
                else:
                    self.vectors[0] = 0

            if next_destin[1] > self.coord[1]:
                self.vectors[1] = 1
            else:
                if next_destin[1] < self.coord[1]:
                    self.vectors[1] = -1
                else:
                    self.vectors[1] = 0

    def set_next_position(self):
        cell = self.get_current_cell()
        step = cell.size / fps
        step_x = self.speed * step * self.vectors[0]
        step_y = self.speed * step * self.vectors[1]
        if step_x > 0:
            self.rect.x = self.rect.x + math.ceil(step_x)
        else:
            self.rect.x = self.rect.x + math.floor(step_x)

        if step_y > 0:
            self.rect.y = self.rect.y + math.ceil(step_y)
        else:
            self.rect.y = self.rect.y + math.floor(step_y)

    def is_destination_x(self, cell):
        if self.destination[0] > self.coord[0]:
            if self.rect.x >= cell.x:
                return True
        else:
            if self.rect.x <= cell.x:
                return True

        return False

    def is_destination_y(self, cell):
        if self.destination[1] > self.coord[1]:
            if self.rect.y >= cell.y:
                return True
        else:
            if self.rect.y <= cell.y:
                return True

        return False

    def draw_path(self, cell_size):
        if self.path:
            for point in self.path:
                cell = self.get_cell(point[0], point[1])
                image = pygame.Surface((self.width * cell_size, self.height * cell_size), pygame.SRCALPHA)
                image.fill(red)
                self.screen.blit(image, [cell.x, cell.y])

    def catch_item(self, item):
        self.inventory.add_items(item, 1)

    def get_inventory_info(self):
        return self.inventory.get_info()
