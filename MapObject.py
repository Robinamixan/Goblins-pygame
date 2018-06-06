from ConstantVariables import *


class MapObject:
    title = ''
    x = 0
    y = 0
    cell_size = 0
    cells = []
    width_cells = 0
    height_cells = 0
    screen = None
    color = (0, 0, 0)

    def __init__(self, title, screen, position, cell_size, width_cells, height_cells):
        self.title = title
        self.screen = screen
        self.x = position[0]
        self.y = position[1]
        self.cell_size = cell_size
        self.width_cells = width_cells
        self.height_cells = height_cells
        self.cells = [0] * width_cells
        for i in range(0, width_cells):
            self.cells[i] = [None] * height_cells
            for j in range(0, height_cells):
                self.cells[i][j] = CellObject(self.x + self.cell_size * i, self.x + self.cell_size * j)

    def get_cell(self, x, y):
        return self.cells[x][y]

    def draw_field(self, tool):
        self.screen.fill(white)

        end_position_x = self.x + self.cell_size * (self.width_cells + 1)
        end_position_y = self.y + self.cell_size * (self.height_cells + 1)
        end_x = self.x + self.cell_size * self.width_cells
        end_y = self.y + self.cell_size * self.height_cells
        for x in range(self.x, end_position_x, self.cell_size):
            tool.line(self.screen, black, (x, self.y), (x, end_y), 1)

        for y in range(self.y, end_position_y, self.cell_size):
            tool.line(self.screen, black, (self.x, y), (end_x, y), 1)

    def update_cells(self):
        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                if not cell.is_empty():
                    map_object = cell.get_object()
                    map_object.update_position()

    def draw_cells(self):
        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                if not cell.is_empty():
                    map_object = cell.get_object()
                    map_object.draw((cell.x, cell.y), self.cell_size)

    def get_cell_by_coord(self, x, y):
        pos = [int((x - self.x) / self.cell_size), int((y - self.y) / self.cell_size)]
        return pos


class CellObject:
    empty = True
    contain = None
    x = 0
    y = 0
    size = map_cell_size

    def __init__(self, x, y):
        self.empty = True
        self.x = x
        self.y = y

    def is_empty(self):
        return self.empty

    def get_object(self):
        return self.contain

    def set_object(self, map_object):
        self.contain = map_object
        self.empty = False

    def clear(self):
        self.contain = None
        self.empty = True
