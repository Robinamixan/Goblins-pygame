from StaticObject import *


class MapObject:
    title = ''
    x = 0
    y = 0
    cell_size = 0
    cells = []
    width_cells = 0
    height_cells = 0
    screen = None
    game_controller = None
    color = (0, 0, 0)

    def __init__(self, title, screen, game_controller, position, cell_size, width_cells, height_cells):
        self.title = title
        self.screen = screen
        self.x = position[0]
        self.y = position[1]
        self.cell_size = cell_size
        self.width_cells = width_cells
        self.height_cells = height_cells
        self.cells = [0] * width_cells

        self.game_controller = game_controller

        for i in range(0, width_cells):
            self.cells[i] = [None] * height_cells
            for j in range(0, height_cells):
                self.cells[i][j] = CellObject(self.x + self.cell_size * i, self.x + self.cell_size * j)

    def draw_field(self, tool):
        self.screen.fill(white)

        end_x = self.x + self.cell_size * self.width_cells
        end_y = self.y + self.cell_size * self.height_cells

        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                rectangle = [
                    cell.x,
                    cell.y,
                    cell.size + 1,
                    cell.size + 1
                ]
                tool.rect(self.screen, dark_green, rectangle)
                tool.rect(self.screen, black, rectangle, 1)

        tool.line(self.screen, red, (self.x, self.y), (self.x, end_y), 2)
        tool.line(self.screen, red, (self.x, self.y), (end_x, self.y), 2)
        tool.line(self.screen, red, (end_x, self.y), (end_x, end_y), 2)
        tool.line(self.screen, red, (end_x, end_y), (self.x, end_y), 2)

    def create_wall(self, point):
        wall = StaticObject('wall_' + str(point[0]) + '_' + str(point[1]), self.screen, self.game_controller, self, point, (1, 1), brow)
        self.game_controller.add_static_object(wall)

    def create_map_from_file(self, file_name):
        file = open(file_name, 'r')
        ind_y = 0
        ind_x = 0
        for line in file:
            for character in line:
                if character == 'w':
                    self.create_wall((ind_x, ind_y))

                if character == '\n':
                    ind_x = 0
                else:
                    ind_x += 1
            ind_y += 1
        file.close()

    def get_cell(self, x, y):
        return self.cells[x][y]

    def get_cell_position_by_coord(self, x, y):
        pos = [int((x - self.x) / self.cell_size), int((y - self.y) / self.cell_size)]

        if pos[0] >= self.width_cells:
            pos[0] = self.width_cells - 1

        if pos[1] >= self.height_cells:
            pos[1] = self.height_cells - 1

        if pos[0] < 0:
            pos[0] = 0

        if pos[1] < 0:
            pos[1] = 0

        return pos


class CellObject:
    passable = True
    contain = []
    x = 0
    y = 0
    size = map_cell_size

    def __init__(self, x, y):
        self.passable = True
        self.contain = []
        self.x = x
        self.y = y

    def is_empty(self):
        return not self.contain

    def is_can_move(self, moved_object):
        if self.passable:
            return True
        else:
            if moved_object == self.contain:
                return True
            else:
                return False

    def get_object(self):
        if self.contain:
            return self.contain[-1]
        else:
            return False

    def set_object(self, map_object, passable=False):
        self.contain.append(map_object)
        if not passable:
            self.passable = False

    def remove_object(self, map_object):
        self.contain.remove(map_object)
        if not map_object.passable:
            self.passable = True
