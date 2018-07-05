import numpy as np
from Networks.Network import *
from Networks.Evolution import *

np.set_printoptions(threshold=np.nan, precision=6, suppress=True)

input = np.array([
#1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1,  0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
                  ])

output = np.array([
#1
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 1],
    [1, 1, 0, 0],
    ])

net = Network('1', 10, 4)
net.add_layer(6)
net.add_layer(5)
net.connect()

net.add_data_set(input, output)

for j in range(30000):
    net.learn()

net.save()
net.print_output()
#
# net = net.load()
#
# C = np.array([
# #1
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1,  0, 0, 0, 0, 0, 0, 0, 0],
#     [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [-1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [-1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
#                   ])
#
# net.activate(C)
# net.print_output()
#
# evolution = Evolution()
# evolution.activate()
# evolution.sort_members()
# evolution.set_children()

c = 4
