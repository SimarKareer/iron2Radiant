import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import imutils
import math
import numpy
from skimage import data
from skimage.feature import match_template


ENEMY_COLOR = [91, 85, 249]#[249, 85, 91]
ME_COLOR = [194, 254, 255]
print(cv2.__version__)

def imgToMap(img):
    """
    Returns a cv2 image object that has the relevant map
    """
    img = cv2.imread(img)
    map_img = img[10:475, 70:455, :]
    print(map_img.shape)
    return map_img


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

def imToObs(map_img, grid_shape, circle_radius, vis=False):
    """
    Take in a map image.  Return list of [("agent", x, y)]
    """
    locs = []
    for agent_template in os.listdir('./templates'):
        #Open template and get canny
        tmp = cv2.imread('./templates/' + agent_template)
        tmp = cv2.Canny(tmp, 10, 25)
        (height, width) = tmp.shape[:2]
        #open the main image and convert it to gray scale image
        gray_image = cv2.cvtColor(map_img, cv2.COLOR_BGR2GRAY)
        temp_found = None
        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            #resize the image and store the ratio
            resized_img = imutils.resize(gray_image, width=int(gray_image.shape[1] * scale))
            ratio = gray_image.shape[1] / float(resized_img.shape[1])
            if resized_img.shape[0] < height or resized_img.shape[1] < width:
                break
            #Convert to edged image for checking
            e = cv2.Canny(resized_img, 10, 25)
            match = cv2.matchTemplate(e, tmp, cv2.TM_CCORR)
            (_, val_max, _, loc_max) = cv2.minMaxLoc(match)
            if temp_found is None or val_max>temp_found[0]:
                temp_found = (val_max, loc_max, ratio)
        #Get information from temp_found to compute x,y coordinate
        (_, loc_max, r) = temp_found
        (x_start, y_start) = (int(loc_max[0]), int(loc_max[1]))
        (x_end, y_end) = (int((loc_max[0] + width)), int((loc_max[1] + height)))
        #Draw rectangle around the template
        if vis == True:
            cv2.rectangle(map_img, (x_start, y_start), (x_end, y_end), (0, 0, 0), 1)
            print(map_img.shape)
            cv2.imwrite('res.png', map_img)
        
        locs.append((agent_template[:-3], (x_start + x_end) / 2, (y_start + y_end) / 2))
        # TODO: Locs are currently in image map coordinates, need to be converted to grid coordinates
    for i in range(len(locs)):
        x_pos = int(locs[i][1])
        y_pos = int(locs[i][2])
        char_map = map_img[y_pos - circle_radius -1:y_pos + circle_radius + 1,
        x_pos - circle_radius - 1: x_pos + circle_radius + 1]
        cv2.imwrite('test.png', char_map)
        min_diff = 442 #maximum L2 norm of two colors
        min_degree = 0
        for degree in range(0, 360, 6):
            theta = math.radians(degree)
            y_loc = circle_radius - math.floor(circle_radius * math.sin(theta))
            x_loc = circle_radius + math.floor(circle_radius * math.cos(theta))
            pix = char_map[y_loc, x_loc, :]
            # diff = pix[0]
            diff = np.linalg.norm(pix - ME_COLOR)

            if diff < min_diff:
                min_degree = degree
                min_diff = diff
        locs[i] = (locs[i][0], x_pos, y_pos, min_degree)
        
    
    
    return locs


