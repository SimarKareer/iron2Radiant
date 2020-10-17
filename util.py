import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

def imgToMap(img):
    """
    Returns a cv2 image object that has the relevant map
    """
    img = cv2.imread(img, 0)
    map = img[20:410, 30:450]
    return map
    cv2.imwrite('testcrop.png', map)


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
    Take in a map image.  Return list of [("agent", x, y)]
    """
    for agent_template in os.listdir('./templates'):
        tmp = cv2.imread('./templates/' + agent_template, 0)
        w, h = tmp.shape[::-1]
        print(map_img.shape)
        print(tmp.shape)
        res = cv2.matchTemplate(map_img,tmp, eval('cv2.TM_CCOEFF_NORMED'))
        threshold = 0.3
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(map_img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        cv2.imwrite('res.png',map_img)

