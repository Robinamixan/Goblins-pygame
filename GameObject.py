from ConstantVariables import *


class GameObject:
    title = ''
    x = 0
    y = 0
    coord = [0, 0]
    width = 0
    height = 0
    screen = None
    map = None
    color = (0, 0, 0)

    x_vector = 0
    y_vector = 0
    destination = []
    path = []

    def __init__(self, title, screen, game_map, position, size, color):
        self.title = title
        self.screen = screen
        self.map = game_map
        self.width = size[0]
        self.height = size[1]
        self.color = color

        self.coord = [position[0], position[1]]

        cell = self.get_current_cell()
        cell.set_object(self)

        self.window_position = [cell.x, cell.y]

    def update(self):
        return None

    def draw(self, cell_size):
        return None

    def get_current_cell(self):
        return self.map.get_cell(self.coord[0], self.coord[1])


class StaticObject(GameObject):
    def __init__(self, title, screen, game_map, position, size, color):
        super().__init__(title, screen, game_map, position, size, color)

    def draw(self, cell_size):
        self.screen.fill(self.color, rect=[
            self.window_position[0],
            self.window_position[1],
            self.width * cell_size,
            self.height * cell_size
        ])


class MobObject(GameObject):
    speed = 1

    def __init__(self, title, screen, game_map, position, size, color, speed=1):
        self.speed = speed

        self.destination = [position[0], position[1]]

        super().__init__(title, screen, game_map, position, size, color)

    def get_destination_cell(self):
        return self.map.get_cell(self.destination[0], self.destination[1])

    def set_destination(self, row, column):
        self.create_path([self.coord[0], self.coord[1]], [row, column])

    def create_path(self, start, end):
        path = []

        step_number = 0
        current_step = start

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

    def go_left(self):
        self.set_destination(self.coord[0] - 1, self.coord[1])

    def go_right(self):
        self.set_destination(self.coord[0] + 1, self.coord[1])

    def go_up(self):
        self.set_destination(self.coord[0], self.coord[1] - 1)

    def go_down(self):
        self.set_destination(self.coord[0], self.coord[1] + 1)

    def stop(self):
        self.path = []

    def update(self):
        if self.path:
            if self.destination == self.coord:
                next_step = self.path[0]
                next_cell = self.map.get_cell(next_step[0], next_step[1])
                if next_cell.is_empty():
                    self.destination = next_step
                    self.update_move()
                else:
                    self.stop()
            else:
                self.update_move()

    def update_move(self):
        self.update_vectors()
        cell = self.get_destination_cell()
        if self.is_destination(cell):
            self.window_position = [cell.x, cell.y]
            self.coord = [self.destination[0], self.destination[1]]
            self.x_vector = 0
            self.y_vector = 0
            self.path.pop(0)
        else:
            self.window_position = self.get_next_position()

    def update_vectors(self):
        cell = self.get_destination_cell()
        if self.window_position[0] > cell.x:
            self.x_vector = -1
        else:
            if self.window_position[0] < cell.x:
                self.x_vector = 1
            else:
                self.x_vector = 0

        if self.window_position[1] > cell.y:
            self.y_vector = -1
        else:
            if self.window_position[1] < cell.y:
                self.y_vector = 1
            else:
                self.y_vector = 0

    def get_next_position(self):
        cell = self.get_current_cell()
        step = cell.size / fps
        next_x = self.window_position[0] + self.speed * step * self.x_vector
        next_y = self.window_position[1] + self.speed * step * self.y_vector
        return [next_x, next_y]

    def is_destination(self, cell):
        is_destination_x = False
        if self.destination[0] > self.coord[0]:
            if self.window_position[0] >= cell.x:
                is_destination_x = True
        else:
            if self.window_position[0] <= cell.x:
                is_destination_x = True

        is_destination_y = False
        if self.destination[1] > self.coord[1]:
            if self.window_position[1] >= cell.y:
                is_destination_y = True
        else:
            if self.window_position[1] <= cell.y:
                is_destination_y = True

        return is_destination_x and is_destination_y

    def draw(self, cell_size):
        self.screen.fill(self.color, rect=[
            self.window_position[0],
            self.window_position[1],
            self.width * cell_size,
            self.height * cell_size
        ])


