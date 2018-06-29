import numpy as np
import _pickle as pickle
import copy
from ConstantVariables import *


class Network:
    def __init__(self, name='', inputs=0, outputs=0):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.layers_info = []
        self.layers = {}
        self.connections = {}
        self.input_data_set = []
        self.output_data_set = []

    def add_layer(self, amount):
        self.layers_info.append(amount)

    def add_data_set(self, input_data_set, output_data_set):
        if len(input_data_set) == len(output_data_set):
            self.input_data_set = input_data_set
            self.output_data_set = output_data_set

    def connect(self):
        self.layers['input'] = 0

        current_layer = self.inputs
        current_layer_name = 'input'
        for index, value in enumerate(self.layers_info):
            self.layers['hidden_' + str(index + 1)] = 0
            self.connections[current_layer_name +'_to_' + 'hidden_' + str(index + 1)] = 2 * np.random.random((current_layer, value)) - 1
            current_layer = value
            current_layer_name = 'hidden_' + str(index + 1)

        self.layers['output'] = 0
        self.connections[current_layer_name +'_to_out'] = 2 * np.random.random((current_layer, self.outputs)) - 1

    def activate(self, input_data):
        if len(input_data) == self.inputs:
            self.layers['input'] = input_data
            current_layer_name = 'input'
            for index, value in enumerate(self.layers_info):
                connections = self.connections[current_layer_name +'_to_' + 'hidden_' + str(index + 1)]

                self.layers['hidden_' + str(index + 1)] = self.nonlin(np.dot(self.layers[current_layer_name], connections))

                current_layer_name = 'hidden_' + str(index + 1)

            connections = self.connections[current_layer_name + '_to_out']
            self.layers['output'] = self.nonlin(np.dot(self.layers[current_layer_name], connections))

    def learn(self, learning_rate=0.05):
        for input_data, output_data in zip(self.input_data_set, self.output_data_set):
            self.activate(input_data)

            l2_error = output_data - self.layers['output']

            # print("Error:" + str(np.mean(np.abs(l2_error))))

            #производная сигмоиды
            # sygmoid = self.nonlin(self.layers['output'], deriv=True)
            # l2_delta = l2_error * sygmoid
            #
            # self.connections['hidden_1_to_out'][0] += self.layers['hidden_1'][0]*l2_delta*learning_rate
            # self.connections['hidden_1_to_out'][1] += self.layers['hidden_1'][1]*l2_delta*learning_rate
            # self.connections['hidden_1_to_out'] += self.layers['hidden_1'].T.dot(l2_delta)
            (self.connections['hidden_1_to_out'], l2_delta) = self.get_weight(
                self.connections['hidden_1_to_out'],
                self.layers['hidden_1'],
                self.layers['output'],
                l2_error,
                learning_rate
            )

            # как сильно значения l1 влияют на ошибки в l2?
            l1_error = l2_delta.dot(self.connections['hidden_1_to_out'].T)

            # в каком направлении нужно двигаться, чтобы прийти к l1?
            # если мы были уверены в предсказании, то сильно менять его не надо
            # l1_delta = l1_error * self.nonlin(self.layers['hidden_1'], deriv=True)

            (self.connections['input_to_hidden_1'], l1_delta) = self.get_weight(
                self.connections['input_to_hidden_1'],
                self.layers['input'],
                self.layers['hidden_1'],
                l1_error,
                learning_rate
            )

            # self.connections['input_to_hidden_1'] += self.layers['input'].T.dot(l1_delta)

    def get_weight(self, connections_layer, start_layer, end_layer, error, learning_rate):
        delta = error * self.nonlin(end_layer, deriv=True)
        for (x, y), connections in np.ndenumerate(connections_layer):
            temp = start_layer[x]
            deltas = delta[y]
            mult = np.dot(deltas, temp)
            connections_layer[x][y] -= mult * learning_rate

        return [connections_layer, delta]

    def print_output(self):
        print(self.layers['output'])

    def nonlin(self, x, deriv=False):
        if deriv:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def save(self):
        with open(networks_directory_save + 'Network_' + self.name + '.dump', 'wb') as output:
            pickle.dump(copy.copy(self), output, -1)

    def load(self):
        with open(networks_directory_save + 'Network_' + self.name + '.dump', 'rb') as input:
            network = pickle.load(input)
            return network
