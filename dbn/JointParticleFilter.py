from ObservationModels import sightDistribution, audioDistribution


class JointParticleFilter:
    def __init__(self, numParticles, gridSize):
        self.gridSize = gridSize
        self.initParticles(numParticles, gridSize)

    def observe(observations, gameState):
        """
        let observations be (visual, sound)
        """
        visual, audio = observations
        visualEmission = sightDistribution(visual) # since this is perfect knowledge just update all particles
        soundEmission = audioDistribution(audio)
        totalWeight = 0

        # For now this can start as just one players position
        currPosition = gameState.getFriendlyPos()

        allPossible = np.zeros(gridSize)

        if emissionModel is not None:
            totalWeight = 0
            for i in range(len(self.particles)):
                distFromParticle = util.euclideanDistance(self.particles[i], currPosition)
                weight = 1 if self.particles[i] == visualEmission else 0
                totalWeight += weight

                allPossible[self.particles[i]] +=  weight
                totalWeight += weight
        
        # newParticles = util.nSample(allPossible, None, self.numParticles)
        # newParticles = []
        # newParticles = np.zeros(self.numParticles, 2)
        
        if totalWeight == 0: 
            self.initParticles(self.numParticles, self.gridSize)
            self.beliefs = self.getBeliefDistribution()
            return

        # for i in range(len(self.numParticles)):
        #     newParticles += [util.sample(allPossible)]
        allPossible = allPossible / np.sum(allPossible) #full grid size with probabilities
        self.beliefs = allPossible

        choices = np.random.choice(len(allPossible), allPossible.flatten()) #Flattened probs
        newParticles = np.zeros(self.numParticles, 2)
        newParticles[:,0] = (choices / self.gridSize[1]).astype(int)
        newParticles[:,1] = (choices % self.gridSize[1]).astype(int)
        
        self.particles = newParticles
    

    def timeElapse(self):

        
        # for i in range(len(self.particles)):
        #     newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, self.particles[i]))
        #     self.particles[i] = util.sample(newPosDist)

    def initParticles(self, numParticles, gridSize)
        """
        return newly initialized particles

        self.legalPositions will be useful
        [
            [x, y],
            [x, y],
            [x, y]
        ]
        """
        X, Y = gridSize
        
        # particles = np.zeros((numParticles, numParticles))
        indices = np.random.choice(len(self.legalPositions), numParticles)
        self.particles = self.legalPositions[indices].copy()

