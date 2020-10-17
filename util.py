import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

def transition(map, agent, currPos):
    """
    
    """


def updateProbs(currPred, obs):
    """
    Update current predictions based on new obserations, and time step
    """

    #for every enemy agent
        # for every tile in map
            # update predictions of being at that tile
            # will need to call transition

def imToObs(map_img):
    """
    Take in an image.  Return list of [("agent", x, y)]
    """
    for agent_template in os.listdir('./templates'):
        tmp = cv.read(agent_template, 0)
        map_img = cv.read(map_img, 0)
        map_gray = cv.cvtColor(map_img, cv.COLOR_BGR2GRAY)
        w, h = tmp.shape[::-1]
        res = cv.matchTemplate(map_gray,tmp,cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(map_img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        cv.imwrite('res.png',map_img)

