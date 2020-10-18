from dbn.JointParticleFilter import JointParticleFilter

class Game:
    def __init__(self, numParticles):
        self.jointParticleFilter = JointParticleFilter(numParticles, [1,1])

    def tick(self, observations):
        print('ping')
        print(observations)
        self.jointParticleFilter.observe(observations)
        self.jointParticleFilter.timeUpdate()

