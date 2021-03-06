import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import imutils
import math
import numpy
from skimage import data
from skimage.feature import match_template
from scipy import stats


ENEMY_COLOR = [91, 85, 249]#[249, 85, 91]
ME_COLOR = [194, 254, 255]
FRIENDLY_COLOR = [252, 253, 152]
GRAY = [146, 149, 146]
VISION = [0,165,255]
template_list = []
for agent_template in os.listdir('./image_templates'):
    template_list.append((cv2.imread('./image_templates/' + agent_template), agent_template[:-4]))

def imgToMap(img, streamMode=True):
    """
    Returns a cv2 image object that has the relevant map
    """
    if streamMode == False:
        img = cv2.imread(img)
    map_img = img[10:475, 70:455, :]
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
    try:
        locs = []
        for tmp, name in template_list:
            #Open template and get canny
            tmp = cv2.Canny(tmp, 10, 25)
            (height, width) = tmp.shape[:2]
            #open the main image and convert it to gray scale image
            gray_image = cv2.cvtColor(map_img, cv2.COLOR_BGR2GRAY)
            temp_found = None
            for scale in np.linspace(0.8, 1.0, 4)[::-1]:
                #resize the image and store the ratio
                resized_img = imutils.resize(gray_image, width=int(gray_image.shape[1] * scale))
                ratio = gray_image.shape[1] / float(resized_img.shape[1])

                #Convert to edged image for checking
                e = cv2.Canny(resized_img, 10, 25)
                match = cv2.matchTemplate(e, tmp, cv2.TM_CCORR_NORMED)
                (_, val_max, _, loc_max) = cv2.minMaxLoc(match)
                #get the best for each scale sizing
                if temp_found is None or val_max>temp_found[0]:
                    temp_found = (val_max, loc_max, ratio)
            #Get information from temp_found to compute x,y coordinate
            (val_max, loc_max, r) = temp_found
            #print(name, val_max)
            if val_max < 0.52:
                continue
            (x_start, y_start) = (int(loc_max[0]), int(loc_max[1]))
            (x_end, y_end) = (int((loc_max[0] + width)), int((loc_max[1] + height)))
            #Draw rectangle around the template
            
            x_pos = round((x_start + x_end) / 2)
            y_pos = round((y_start + y_end) / 2)
            char_map = map_img[y_pos - circle_radius -1:y_pos + circle_radius + 1,
            x_pos - circle_radius - 1: x_pos + circle_radius + 1]

            bluest = (442, 0, 0)
            reddest = (442, 0, 0)

            for degree in range(0, 360, 6):
                theta = math.radians(degree)
                y_loc = circle_radius - math.floor(circle_radius * math.sin(theta))
                x_loc = circle_radius + math.floor(circle_radius * math.cos(theta))
                pix = char_map[y_loc, x_loc, :]

                blue_diff = np.linalg.norm(pix - FRIENDLY_COLOR)
                red_diff = np.linalg.norm(pix - ENEMY_COLOR)
                if blue_diff < bluest[0]:
                    bluest = (blue_diff, degree, pix)
                if red_diff < reddest[0]:
                    reddest = (red_diff, degree, pix)                

            if name[-1] == 'b' and (reddest[0] < bluest[0]):
                continue
            if name[-1] == 'r' and (bluest[0] < reddest[0]):
                continue
            best_pix = bluest[2]
            min_degree = bluest[1]
            if reddest[0] < bluest[0]:
                min_degree = reddest[1]
                best_pix = reddest[2]
            if vis == True:
                cv2.rectangle(map_img, (x_start, y_start), (x_end, y_end), (0, 0, 0), 1)
                cv2.imwrite('res.png', map_img)

            # TODO: Locs are currently in image map coordinates, need to be converted to grid coordinates
            adjusted_x_pos = int((x_pos-14)/3.6)
            adjusted_y_pos = int((y_pos-14)/3.6)
            locs.append((name, adjusted_x_pos, adjusted_y_pos, min_degree))
            
    except Exception as e:
        print(e)
    print(locs)
    return locs


def findVisionCones(map_img):
    """
    Take in a map image.  Return 2D array of True/False based on where vision cones are
    """
    map_img = map_img[14:-15, 14:-14]

    white_lo=np.array([176,176,176])
    white_hi=np.array([180,180,180])

    # Mask image to only select whites
    mask=cv2.inRange(map_img,white_lo,white_hi)

    # Change image to black where we found white
    map_img[mask>0]=VISION

    # cv2.imwrite("test_cell.png",map_img)

    y_dim = 120
    x_dim = 100
    y_chunk = map_img.shape[0] / y_dim
    x_chunk = map_img.shape[1] / x_dim
    vision_cones = np.zeros([y_dim, x_dim])
    for y in range(0, y_dim - 1):
        for x in range(0, x_dim - 1):
            cell = map_img[math.floor(y*y_chunk):math.floor(y*y_chunk + y_chunk), math.floor(x*x_chunk):math.floor(x*x_chunk + x_chunk)]
            # cv2.imwrite('cell_images/test_cell' + str(x) + ',' + str(y) + '.png', cell)
            val_dict = {}
            for row in cell:
                for val in row:
                    if tuple(val) in val_dict:
                        val_dict[tuple(val)] += 1
                    else:
                        val_dict[tuple(val)] = 1
            mode_val = list(max(val_dict, key = val_dict.get))
            if mode_val == VISION:
                vision_cones[y][x] = 1
    return vision_cones
