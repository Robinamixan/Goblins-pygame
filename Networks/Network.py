import numpy as np


class Network:
    inputs = 0
    layers_info = []
    layers = {}
    connections = {}
    outputs = 0

    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    def add_layer(self, amount):
        self.layers_info.append(amount)

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

    def nonlin(self, x, deriv=False):
        if deriv:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))
