from ParticleFilter import ParticleFilter
from MapLoader import getGrid, getLegalPos

class Game:
    def __init__(self, map_path, numParticles, names):
        legalPos = getLegalPos(getGrid(map_path))
        self.particleFilters = {name: particleFilter(numParticles, [120,100], legalPos) for name in names}
        # self.particleFilter = particleFilter(numParticles, [1,1])

    def tick(self, observations):
        print('ping')
        print(observations)

        for observation in observations:
            name, x, y, theta = observation
            self.particleFilters[name].observe((x, y, theta))
            self.particleFilter.timeElapse()

    def getBeliefDist(self):
        return [particleFilter.getBeliefDist() for particleFilter in self.particleFilters.values()]

