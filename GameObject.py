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
    speed = 1
    x_vector = 0
    y_vector = 0
    destination = []

    def __init__(self, title, screen, game_map, position, size, color, speed=1):
        self.title = title
        self.screen = screen
        self.map = game_map
        self.x = position[0]
        self.y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.speed = speed

        self.destination = [self.x, self.y]
        self.coord = [self.x, self.y]

        cell = self.get_current_cell()
        cell.set_object(self)

        self.window_position = [cell.x, cell.y]

    def update_position(self):
        if self.destination != self.coord:
            cell = self.get_destination_cell()
            if not self.is_destination(cell):
                self.update_vectors()
                self.window_position = self.get_next_position()
            else:
                self.window_position = [cell.x, cell.y]
                self.coord = [self.destination[0], self.destination[1]]
                self.x_vector = 0
                self.y_vector = 0

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

    def draw(self, start_position, cell_size):
        self.screen.fill(self.color, rect=[
            self.window_position[0],
            self.window_position[1],
            self.width * cell_size,
            self.height * cell_size
        ])

    def get_current_cell(self):
        return self.map.get_cell(self.coord[0], self.coord[1])

    def get_destination_cell(self):
        return self.map.get_cell(self.destination[0], self.destination[1])

    def set_destination(self, row, column):
        if self.destination != [row, column]:
            if self.destination[0] > row:
                self.x_vector = -1
            else:
                if self.destination[0] < row:
                    self.x_vector = 1
                else:
                    self.x_vector = 0

            if self.destination[1] > column:
                self.y_vector = -1
            else:
                if self.destination[1] < column:
                    self.y_vector = 1
                else:
                    self.y_vector = 0
        self.destination = [row, column]

    def check_edge_collision(self, edge):
        (x_p, y_p) = self.get_next_position()
        if x_p + self.width > edge[0] or x_p < 0:
            self.prevent_horizontal()

        if y_p + self.height > edge[1] or y_p < 0:
            self.prevent_vertical()

    def prevent_horizontal(self):
        # self.x_vector = 0
        self.x_vector *= -1

    def prevent_vertical(self):
        # self.y_vector = 0
        self.y_vector *= -1

    def go_left(self):
        self.set_destination(self.coord[0] - 1, self.coord[1])

    def go_right(self):
        self.set_destination(self.coord[0] + 1, self.coord[1])

    def stop_horizontal(self):
        self.x_vector = 0

    def go_up(self):
        self.set_destination(self.coord[0], self.coord[1] - 1)

    def go_down(self):
        self.set_destination(self.coord[0], self.coord[1] + 1)

    def stop_vertical(self):
        self.y_vector = 0
