import numpy as np

# 0 wall, 1 normal, 2 blue, 3 red, 4 green

color_dict = {
    0: []
    1: [1]
}

class TransformationFunction:
    def __init__(self, transformation_path):
        self.flag = flag

        with open(transformation_path, 'rb') as handle:
            self.map = pickle.load(handle)


    def 