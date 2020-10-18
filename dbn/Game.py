from dbn.ParticleFilter import ParticleFilter
from dbn.MapLoader import getGrid, getLegalPos

class Game:
    def __init__(self, map_path, numParticles, names):
        legalPos = getLegalPos(getGrid(map_path))
        transitionPath = "dbn/bind100.db"
        self.particleFilters = {name: ParticleFilter(numParticles, [120,100], transitionPath, legalPos) for name in names}
        self.first = True
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

                print("SHouldnt see this")
                self.particleFilters[name].observe((x, y, theta))
                self.first = False
                # you don't need to do a vision code update here.  Since seeing an agent will collapse it to one point anyways
            else:
                print("Should see this")
                # Try time epoch first to allow true particles to escape
                self.particleFilters[name].timeElapse()

                if not self.first:
                    self.particleFilters[name].visionConeObserve(visionCones)

    def getBeliefDist(self):
        return [(name, particleFilter.getBeliefDistribution()) for name, particleFilter in self.particleFilters.items()]

