import numpy as np
import _pickle as pickle
import copy

from collections import OrderedDict
from ConstantVariables import *
from pathlib import Path


class Network:
    def __init__(self, name='', inputs=0, outputs=0):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.layers_info = []
        self.layers = {}
        self.connections = OrderedDict()
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
            self.layers['hidden_' + str(index)] = 0
            self.connections[current_layer_name +'_to_' + 'hidden_' + str(index)] = 2 * np.random.random((current_layer, value)) - 1
            current_layer = value
            current_layer_name = 'hidden_' + str(index)

        self.layers['output'] = 0
        self.connections[current_layer_name +'_to_output'] = 2 * np.random.random((current_layer, self.outputs)) - 1

    def activate(self, input_data):
        self.layers['input'] = input_data
        current_layer_name = 'input'
        for index, value in enumerate(self.layers_info):
            connections = self.connections[current_layer_name +'_to_' + 'hidden_' + str(index)]

            self.layers['hidden_' + str(index)] = self.sigmoid(np.dot(self.layers[current_layer_name], connections))

            current_layer_name = 'hidden_' + str(index)

        connections = self.connections[current_layer_name + '_to_output']
        self.layers['output'] = self.sigmoid(np.dot(self.layers[current_layer_name], connections))

    def learn(self, learning_rate=0.1):
        self.activate(self.input_data_set)

        l2_error = self.output_data_set - self.layers['output']
        print("Error:" + str(np.mean(np.abs(l2_error))))

        error = l2_error
        delta = None
        for name in reversed(self.connections):
            start, end = name.split('_to_')

            self.connections[name], delta = self.get_weight(
                self.connections[name],
                self.layers[start],
                self.layers[end],
                error,
                learning_rate
            )

            error = delta.dot(self.connections[name].T)

    def get_weight(self, connections_layer, start_layer, end_layer, error, learning_rate):
        delta = error * self.sigmoid(end_layer, deriv=True)

        connections_layer += start_layer.T.dot(delta) * learning_rate

        return connections_layer, delta

    def print_output(self, converted=False):
        output = self.get_output(convert=converted)
        if converted:
            if output.shape == (4,):
                if output[0]:
                    print('up')
                if output[1]:
                    print('right')
                if output[2]:
                    print('down')
                if output[3]:
                    print('left')
            else:
                for result in output:
                    print(result)
                    if result[0]:
                        print('up')
                    if result[1]:
                        print('right')
                    if result[2]:
                        print('down')
                    if result[3]:
                        print('left')
                    print('---------')
        else:
            print(self.layers['output'])

    def convert_output(self):
        if len(self.layers['output'].shape) > 1:
            for (x, y), result in np.ndenumerate(self.layers['output']):
                if result > 0.6:
                    self.layers['output'][x][y] = 1
                else:
                    self.layers['output'][x][y] = 0
        else:
            for x, result in np.ndenumerate(self.layers['output']):
                if result > 0.6:
                    self.layers['output'][x] = 1
                else:
                    self.layers['output'][x] = 0

    def get_output(self, convert=False):
        if convert:
            self.convert_output()
        return self.layers['output']

    def sigmoid(self, x, deriv=False):
        if deriv:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def save(self):
        with open(networks_directory_save + 'Network_' + self.name + '.dump', 'wb') as output:
            pickle.dump(copy.copy(self), output, -1)

    def load(self):
        file = Path(networks_directory_save + 'Network_' + self.name + '.dump')
        if file.exists():
            with open(networks_directory_save + 'Network_' + self.name + '.dump', 'rb') as input:
                network = pickle.load(input)
                return network
        else:
            with open(networks_directory_save + 'Network_1.dump', 'rb') as input:
                network = pickle.load(input)
                network.name = self.name
                # network.save()
                return network
