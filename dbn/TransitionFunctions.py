import numpy as np
import pickle

# 0 wall, 1 normal, 2 blue, 3 red, 4 green

class TransitionFunction:
    def __init__(self, transition_path):
        with open(transition_path, 'rb') as handle:
            self.map = pickle.load(handle)

    def getPosDist(self, coord, mode='uniform'):
        ''' coord is (y, x) '''
        if mode == 'uniform':
            locs = self.map.get(coord)

            probs = np.ones(len(locs)) / len(locs)
            return locs, probs
