from dbn.ObservationModels import sightDistribution, audioDistribution
from dbn.TransitionFunctions import TransitionFunction
import numpy as np

class ParticleFilter:
    def __init__(self, numParticles, gridSize, transition_path, legalPositions):
        self.gridSize = gridSize
        self.numParticles = numParticles
        self.legalPositions = legalPositions
        self.transitionFunction = TransitionFunction(transition_path)
        self.particles = None
        self.initParticles(numParticles, gridSize)

    def observe(self, observations, gameState, visionCones):
        """
        let observations be (visual, sound)

        TODO: sound
        """
        # visual, audio = observations
        # visualEmission = sightDistribution(visual) # since this is perfect knowledge just update all particles
        # soundEmission = audioDistribution(audio)
        if observations:
            y, x, theta = observations
            visualEmission = np.array([y, x])
            totalWeight = 0

            # For now this can start as just one players position
            # currPosition = gameState.getFriendlyPos() # TODO: FOR SOUND

            allPossible = np.zeros(self.gridSize)

            for i in range(len(self.particles)):
                # distFromParticle = util.euclideanDistance(self.particles[i], currPosition) TODO: Only for sound
                weight = 1 if (self.particles[i] == visualEmission).all() else 0
                # if (self.particles[i] == visualEmission).all():
                    # print("GOT A MATCHING PARTICLE")
                if visionCones is not None and self.particles[i] != visualEmission:
                    for visionCone in visionCones:
                        if visionCones[self.particles[i]]:
                            weight=0
                            break

                totalWeight += weight
                y, x = self.particles[i]
                allPossible[int(y), int(x)] +=  weight
        
        # newParticles = util.nSample(allPossible, None, self.numParticles)
        # newParticles = []
        # newParticles = np.zeros(self.numParticles, 2)
        
        if totalWeight == 0:
            print("TOTAL WEIGHT ZERO")
            self.initParticles(self.numParticles, self.gridSize, visualEmission)
            self.beliefs = self.getBeliefDistribution()
            return

        # for i in range(len(self.numParticles)):
        #     newParticles += [util.sample(allPossible)]
        allPossible = allPossible / np.sum(allPossible) #full grid size with probabilities
        self.beliefs = allPossible


        choices = np.random.choice(allPossible.size, self.numParticles, p=allPossible.flatten()) #Flattened probs
        # print("samples", len(choices), "samples")
        newParticles = np.zeros((self.numParticles, 2))
        newParticles[:,1] = (choices / self.gridSize[1]).astype(int)
        newParticles[:,0] = (choices % self.gridSize[1]).astype(int)
        
        self.particles = newParticles
    

    def timeElapse(self):
        ''' [ [x,y], [x,y] ]'''
        print('particle length', len(self.particles))
        for i in range(len(self.particles)):
            y, x  = self.particles[i]
            posDist, probs = self.transitionFunction.getPosDist((int(y), int(x)))

            if len(posDist) == 0:
                self.particles[i] = self.particles[i-1]
                print("lost a particle somewhere")
            else:
                index = np.random.choice(len(posDist), p=probs)
                self.particles[i] = posDist[index].astype(int)


    def getBeliefDistribution(self):
        """
          Return the agent's current belief state, a distribution over
          ghost locations conditioned on all evidence and time passage. This method
          essentially converts a list of particles into a belief distribution (a Counter object)
        """
        "*** YOUR CODE HERE ***"
        distribution = np.zeros(self.gridSize)

        # print('BELLL', self.particles)

        for i in range(len(self.particles)):
            y, x = self.particles[i].astype(int)
            distribution[y][x] += 1

        distribution /= distribution.sum()

        return distribution

    def initParticles(self, numParticles, gridSize, visualEmission=None):
        """
        return newly initialized particles

        self.legalPositions will be useful
        [
            [x, y],
            [x, y],
            [x, y]
        ]
        """

        if visualEmission is not None:
            particles = np.ones((numParticles, 2))
            particles[:,1] *= visualEmission[0]
            particles[:,0] *= visualEmission[1]
            self.particles = particles.astype(int)
            return

        X, Y = gridSize

        print('legal shape', self.legalPositions.shape)
        
        particles = np.zeros((numParticles, 2))
        indices = np.random.choice(len(self.legalPositions), numParticles)
        self.particles = self.legalPositions[indices].copy().astype(int)

