from ConstantVariables import *


class GameObject:
    title = ''
    window_position = []
    coord = [0, 0]
    width = 0
    height = 0
    screen = None
    map = None
    color = (0, 0, 0)

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
    vectors = [0, 0]
    destination = []
    path = []

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
        cell = self.get_destination_cell()
        self.window_position = [cell.x, cell.y]
        self.coord = [self.destination[0], self.destination[1]]
        self.vectors[0] = 0
        self.vectors[1] = 0

    def update(self):
        if self.path:
            if self.destination == self.coord:
                next_step = self.path[0]
                next_cell = self.map.get_cell(next_step[0], next_step[1])
                if next_cell.is_empty():
                    current_cell = self.map.get_cell(self.coord[0], self.coord[1])
                    current_cell.clear()
                    next_cell.set_object(self)
                    self.destination = next_step
                    self.update_move()

                else:
                    self.stop()
            else:
                self.update_move()
        else:
            self.stop()

    def update_move(self):
        cell = self.get_destination_cell()
        if self.is_destination_x(cell) and self.is_destination_y(cell):
            # self.window_position = [cell.x, cell.y]
            self.coord = [self.destination[0], self.destination[1]]
            self.path.pop(0)
            self.update_vectors_in_wait_position()
        else:
            if self.is_destination_x(cell):
                self.window_position[0] = cell.x
                self.coord[0] = self.destination[0]

            if self.is_destination_y(cell):
                self.window_position[1] = cell.y
                self.coord[1] = self.destination[1]

            self.update_vectors(cell)
            self.window_position = self.get_next_position()

    def update_vectors(self, cell):
        if self.window_position[0] > cell.x:
            self.vectors[0] = -1
        else:
            if self.window_position[0] < cell.x:
                self.vectors[0] = 1
            else:
                self.vectors[0] = 0

        if self.window_position[1] > cell.y:
            self.vectors[1] = -1
        else:
            if self.window_position[1] < cell.y:
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
                self.vectors[1] = -1
            else:
                if next_destin[1] < self.coord[1]:
                    self.vectors[1] = 1
                else:
                    self.vectors[1] = 0

    def get_next_position(self):
        cell = self.get_current_cell()
        step = cell.size / fps
        next_x = self.window_position[0] + self.speed * step * self.vectors[0]
        next_y = self.window_position[1] + self.speed * step * self.vectors[1]
        return [next_x, next_y]

    def is_destination_x(self, cell):
        if self.destination[0] > self.coord[0]:
            if self.window_position[0] >= cell.x:
                return True
        else:
            if self.window_position[0] <= cell.x:
                return True

        return False

    def is_destination_y(self, cell):
        if self.destination[1] > self.coord[1]:
            if self.window_position[1] >= cell.y:
                return True
        else:
            if self.window_position[1] <= cell.y:
                return True

        return False

    def draw(self, cell_size):
        self.screen.fill(self.color, rect=[
            self.window_position[0],
            self.window_position[1],
            self.width * cell_size,
            self.height * cell_size
        ])


