from .math import *


class Net:
    def __init__(self, number_of_layers=2, size_of_layers=2, func=filt):
        self.activation = func
        self.layer_weights = [
            [[0]*size_of_layers for j in range(size_of_layers)]
            for i in range(number_of_layers - 1)
        ]
        self.number_of_layers = number_of_layers
        self.size_of_layers = size_of_layers
        self.name = 'name_me_plz'

    def randomize(self):
        for i in range(self.number_of_layers - 1):
            for j in range(self.size_of_layers):
                for k in range(self.size_of_layers):
                    self.layer_weights[i][j][k] = seed()

    def save(self, name=''):
        if name == '':
            name = self.name
        f = open(name, 'w')
        f.writelines(["{} {}".format(self.number_of_layers, self.size_of_layers)])
        f.write("\n")
        for i in self.layer_weights:
            for j in i:
                print(*j, file=f)
        f.close()
        self.name = name

    def load(self, path=''):
        if path == '':
            path = self.name
        f = open(path, 'r')
        self.number_of_layers, self.size_of_layers = map(int, f.readline().split())
        self.layer_weights = [
            [
                list(map(float, f.readline().split())) for j in range(self.size_of_layers)
            ]
            for i in range(self.number_of_layers - 1)
        ]
        f.close()
        self.name = path
        return self.extract_dna()

    def show(self):
        for i in self.layer_weights:
            for j in i:
                print(*j)

    def run(self, data):
        data = self.activation(data)
        for weights in self.layer_weights:
            data = mult(weights, data)
            data = self.activation(data)
        return data

    def extract_dna(self):
        dna = []
        for i in self.layer_weights:
            for j in i:
                for k in j:
                    dna.append(k)
        return dna

    def insert_dna(self, dna):
        for i in range(self.number_of_layers - 1):
            for j in range(self.size_of_layers):
                for k in range(self.size_of_layers):
                    self.layer_weights[i][j][k] = \
                        dna[i*(self.size_of_layers**2) + j*self.size_of_layers + k]




