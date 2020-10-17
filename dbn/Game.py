from JointParticleFilter import JointParticleFilter

class Game:
    def __init__(self, numParticles):
        self.jointParticleFilter = JointParticleFilter(numParticles)

    def tick(self, observations):
        self.jointParticleFilter.observe(observations)
        self.jointParticleFilter.timeUpdate()

