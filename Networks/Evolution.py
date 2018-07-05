import json
import random
from Networks.Network import *


class Evolution:
    def __init__(self):
        self.generation = {}
        self.next_generation = {}
        self.need_replace = {}
        self.need_mutate = {}
        self.amount_members = 0

    def add_generation_member(self, network, scope):
        self.amount_members += 1
        self.generation[self.amount_members] = {}
        self.generation[self.amount_members]['network'] = network
        self.generation[self.amount_members]['scope'] = scope

    def add_member(self, destination, index, network, scope):
        if destination == 'generation':
            self.generation[index] = {}
            self.generation[index]['network'] = network
            self.generation[index]['scope'] = scope
        elif destination == 'next_generation':
            self.next_generation[index] = {}
            self.next_generation[index]['network'] = network
            self.next_generation[index]['scope'] = scope
        elif destination == 'need_replace':
            self.need_replace[index] = {}
            self.need_replace[index]['network'] = network
            self.need_replace[index]['scope'] = scope
        elif destination == 'need_mutate':
            self.need_mutate[index] = {}
            self.need_mutate[index]['network'] = network
            self.need_mutate[index]['scope'] = scope

    def get_best(self):
        best_index = 0
        max_scope = 0
        network = None
        for index, item in self.generation.items():
            if float(item['scope']) > max_scope:
                best_index = index
                max_scope = float(item['scope'])
                network = item['network']
        self.generation[best_index]['scope'] = '0'
        return max_scope, network

    def activate(self):
        file = open('rate.txt', 'r')
        for json_string in file:
            result = json.loads(json_string)
            network = Network(result['title'], 8, 4)
            network = network.load()
            self.add_generation_member(network, result['time'])
        file.close()

    def sort_members(self):
        scope, network = self.get_best()
        self.add_member('next_generation', 0, network, scope)

        scope, network = self.get_best()
        self.add_member('next_generation', 1, network, scope)

        scope, network = self.get_best()
        self.add_member('need_replace', 0, network, scope)

        scope, network = self.get_best()
        self.add_member('need_replace', 1, network, scope)

        scope, network = self.get_best()
        self.add_member('need_mutate', 0, network, scope)

    def set_children(self):
        first_parent = self.next_generation[0]['network']
        second_parent = self.next_generation[1]['network']

        first_parent.name = self.need_replace[0]['network'].name
        second_parent.name = self.need_replace[1]['network'].name

        for first_name, first_connection in first_parent.connections.items():
            for second_name, second_connection in second_parent.connections.items():
                if first_name == second_name:
                    first_parts = np.array_split(first_connection, 4)
                    second_parts = np.array_split(second_connection, 4)

                    temp = first_parts[1]
                    first_parts[1] = second_parts[1]
                    second_parts[1] = temp

                    temp = first_parts[3]
                    first_parts[3] = second_parts[3]
                    second_parts[3] = temp

                    first_changed = np.concatenate(first_parts, axis=0)
                    second_changed = np.concatenate(first_parts, axis=0)

                    first_parent.connections[first_name] = first_changed
                    second_parent.connections[second_name] = second_changed

                    first_parent.save()
                    second_parent.save()

        mutant = self.next_generation[0]['network']
        name = self.need_mutate[0]['network'].name
        self.mutate(mutant, name, 0.5)

        mutant = self.next_generation[1]['network']
        name = self.next_generation[1]['network'].name
        self.mutate(mutant, name, 0.001)

    def mutate(self, mutant, name, index):
        mutant.name = name
        amount = random.randint(0, 16)

        for name, connection in mutant.connections.items():
            changed = connection + connection * random.uniform(-index, index)

            mutant.connections[name] = changed

            mutant.save()