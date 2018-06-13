import random
import json


width_cells = 15
height_cells = 15
cells = [0] * width_cells
for i in range(0, width_cells):
    cells[i] = [0] * height_cells
    for j in range(0, width_cells):
        cells[i][j] = 0

json_data = json.dumps(cells)
f = 4
