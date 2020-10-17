class JointParticleFilter:
    def __init__(self, numParticles, gridSize):
        self.particles = self.initParticles(numParticles, gridSize)

    def observe(observations):
        pass

    def timeElapse(self):
        pass

    def initParticles(self, numParticles, gridSize)
        """
        return newly initialized particles
        """
        X, Y = gridSize
        
        particles = np.zeros((5, numParticles, numParticles))

        
