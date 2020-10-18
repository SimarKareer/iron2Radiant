from dbn.ObservationModels import sightDistribution, audioDistribution
from dbn.TransitionFunctions import TransitionFunction
import numpy as np

class ParticleFilter:
    def __init__(self, numParticles, gridSize, transition_path, legalPositions):
        self.gridSize = gridSize
        self.numParticles = numParticles
        self.legalPositions = legalPositions
        # print("HULOOOO?")
        self.initParticles(numParticles, gridSize)
        self.transitionFunction = TransitionFunction(transition_path)

    def visionConeObserve(self, visionCones):
        # print("TEST AHOWE")
        allPossible = self.getBeliefDistribution()
        # print('PPPP', self.particles)
        # print((allPossible == 0).sum())

        totalWeight = 0

        if self.particles is None:
            print("reseting particles")
            self.initParticles(self.numParticles, self.gridSize)


        if visionCones is not None:
            for i in range(len(self.particles)):
                # print('vision cone', visionCones.shape, self.particles[i], i)
                y, x = self.particles[i].astype(int)
                if visionCones[y, x]:
                    allPossible[y, x] = 0
                else:
                    totalWeight += allPossible[y, x]

        allPossible = allPossible / np.sum(allPossible) #full grid size with probabilities
        self.beliefs = allPossible

        # print('Probabilities HELP', allPossible)
        choices = np.random.choice(allPossible.size, self.numParticles, p=allPossible.flatten()) #Flattened probs
        # print("samples", len(choices), "samples")
        ## LOOK AT OTHER CODE
        newParticles = np.zeros((self.numParticles, 2))
        newParticles[:,0] = (choices / self.gridSize[1]).astype(int)
        newParticles[:,1] = (choices % self.gridSize[1]).astype(int)
        
        self.particles = newParticles

    def observe(self, observations):
        """
        let observations be (visual, sound)

        TODO: sound
        """
        totalWeight = 0
        allPossible = np.zeros(self.gridSize)
        visualEmission = None

        if observations is not None:
            y, x, theta = observations
            visualEmission = np.array([y, x])

            # For now this can start as just one players position
            # currPosition = gameState.getFriendlyPos() # TODO: FOR SOUND

            for i in range(len(self.particles)):
                # distFromParticle = util.euclideanDistance(self.particles[i], currPosition) TODO: Only for sound
                weight = 1 if (self.particles[i] == visualEmission).all() else 0
                # totalWeight += weight
                y, x = self.particles[i].astype(int)
                allPossible[y, x] +=  weight
        
        
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

        # print('YOLO AAAAAA')
        
        self.particles = newParticles
    

    def timeElapse(self):
        ''' [ [x,y], [x,y] ]'''
        # print('particle length', len(self.particles))
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
        # if self.particles is None:
        #     self.initParticles(self.numParticles, self.gridSize)
        # print("PEEK PARTICLES ON GET BELIEF DIST",  self.particles[:5])
        # for i in range(len(self.particles)):
        #     if self.particles[i][0] >= 120 or self.particles[i][1] >= 100:
        #         print("ILLEGAL PARTICLE IN BELIEF DIST")

        distribution = np.zeros(self.gridSize)

        for i in range(len(self.particles)):
            y, x = self.particles[i].astype(int)
            # if y >= 120:
            #     y = 119
            # if x >= 100:
            #     x = 99
            
            if y >= 120 or x >= 100:
                index = np.random.choice(len(self.legalPositions))
                self.particles[i] = self.legalPositions[index]
                y, x = self.particles[i].astype(int)
                # print('ILLEGAL', self.particles[i])
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
        print("INIT PARTICLE CALL")

        if visualEmission is not None:
            particles = np.ones((numParticles, 2))
            particles[:,1] *= visualEmission[0]
            particles[:,0] *= visualEmission[1]
            self.particles = particles.astype(int)
            return

        X, Y = gridSize

        print('legal shape', self.legalPositions.shape)

        for i in range(len(self.legalPositions)):
            if self.legalPositions[i][0] >= 120 or self.legalPositions[i][1] >= 100:
                print('Illegal pos at ', self.legalPositions[i], i)
        
        particles = np.zeros((numParticles, 2))
        indices = np.random.choice(len(self.legalPositions), numParticles)
        self.particles = self.legalPositions[indices].copy().astype(int)
        for i in range(len(self.particles)):
            if self.particles[i][0] >= 120 or self.particles[i][1] >= 100:
                print("ILLEGAL PARTICLE")

        print("PEEK PARTICLES ON INIT PARTICLES",  self.particles[:5])

