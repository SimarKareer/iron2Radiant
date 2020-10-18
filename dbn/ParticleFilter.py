from dbn.ObservationModels import sightDistribution, audioDistribution
from dbn.TransitionFunctions import TransitionFunction
import numpy as np

class ParticleFilter:
    def __init__(self, numParticles, gridSize, transition_path, legalPositions):
        self.gridSize = gridSize
        self.legalPositions = legalPositions
        self.transitionFunction = TransitionFunction(transition_path)
        self.initParticles(numParticles, gridSize)

    def observe(observations, gameState, visionCones):
        """
        let observations be (visual, sound)

        TODO: sound
        """
        # visual, audio = observations
        # visualEmission = sightDistribution(visual) # since this is perfect knowledge just update all particles
        # soundEmission = audioDistribution(audio)
        if observations:
            x, y, theta = observations
            visualEmission = np.array([x, y])
            totalWeight = 0

            # For now this can start as just one players position
            # currPosition = gameState.getFriendlyPos() # TODO: FOR SOUND

            allPossible = np.zeros(self.gridSize)

            for i in range(len(self.particles)):
                # distFromParticle = util.euclideanDistance(self.particles[i], currPosition) TODO: Only for sound
                weight = 1 if self.particles[i] == visualEmission else 0
                if visionCones is not None and self.particles[i] != visualEmission:
                    for visionCone in visionCones:
                        if visionCones[self.particles[i]]:
                            weight=0
                            break

                totalWeight += weight
                allPossible[self.particles[i]] +=  weight
        
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
        ''' [ [x,y], [x,y] ]'''
        for i in range(len(self.particles)):
            x, y  = self.particles[i]
            posDist, probs = self.transitionFunction.getPosDist((x, y))
            self.particles[i] = np.random.choice(posDist, p=probs)


    def getBeliefDistribution(self):
        """
          Return the agent's current belief state, a distribution over
          ghost locations conditioned on all evidence and time passage. This method
          essentially converts a list of particles into a belief distribution (a Counter object)
        """
        "*** YOUR CODE HERE ***"
        distribution = np.zeros(self.gridSize)

        for particle in self.particles:
            distribution[particle] += 1

        distribution /= distribution.sum()

        return distribution

    def initParticles(self, numParticles, gridSize):
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
        
        particles = np.zeros((numParticles, numParticles))
        indices = np.random.choice(len(self.legalPositions), numParticles)
        self.particles = self.legalPositions[indices].copy()

