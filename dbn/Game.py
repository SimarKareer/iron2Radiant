from dbn.ParticleFilter import ParticleFilter
from dbn.mapLoader import getGrid, getLegalPos

class Game:
    def __init__(self, map_path, numParticles, names):
        legalPos = getLegalPos(getGrid(map_path))
        transitionPath = "dbn/bind100.db"
        self.particleFilters = {name: ParticleFilter(numParticles, [120,100], transitionPath, legalPos) for name in names}
        # self.particleFilter = particleFilter(numParticles, [1,1])

    def tick(self, observations, visionCones):
        print(observations)
        # print(self.particleFilters["sage"].particles)

        obsNames = []

        for observation in observations:
            name, x, y, theta = observation
            obsNames.append(name)

        for name, particleFilter in self.particleFilters.items():
            if name + '_r' in obsNames:
                idx = obsNames.index(name + '_r')
                obsName, x, y, theta = observations[idx]

                self.particleFilters[name].observe((x, y, theta), None, visionCones)
            else:
                self.particleFilters[name].timeElapse()

    def getBeliefDist(self):
        return [(name, particleFilter.getBeliefDistribution()) for name, particleFilter in self.particleFilters.items()]

