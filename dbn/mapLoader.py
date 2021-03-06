from PIL import Image
import numpy as np


def getGrid(map_path):
    # load the image
    image = Image.open(map_path)
    # convert image to numpy array
    data = np.asarray(image.convert('L'))
    unique_values = np.unique(data.flatten())

    grid = data.copy()

    count = 1
    for val in unique_values:
        if val == 255:
            grid[data == val] = 0
        else:
            print(val, count)
            grid[data == val] = count
            count += 1 
    
    return grid

def gridToImg(grid, factor=50):
    grid = grid * grid * factor
    Image.fromarray(grid).save('dbn/temp.png')
    
def getLegalPos(grid):
    # [ [x,y] ]
    pos = []
    
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x][y] != 0:
                pos.append([x, y])

    return np.array(pos)

def main():
    img = getGrid("dbn/bind100.png")
    gridToImg(img)
    print(getLegalPos(img)[:8])
    # print(img[0], img[:,0])

if __name__ == "__main__":
    main()
