import pickle
import numpy as np
from dbn.MapLoader import getGrid
    

# Currently fixed movement to 1 since movement isn't computed shortest to longest distance
# Otherwise, could move through walls
# Future flag can be used to generate function per agent
def preprocess(grid, path, movement=5, flag=0):
    mapping = {}

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            curr = grid[y][x]
            allowed = []
            # if curr == 0:
            #     continue
            for h in range(-movement, movement + 1):
                for w in range(-movement, movement + 1):
                    if y + h < 0 or y + h >= grid.shape[0] or x + w < 0 or x + w >= grid.shape[1]:
                        continue

                    nxt = grid[y + h][x + w]
                    
                    # Don't allow moving in walls, onto boyes, xes one wax for teleport and heaven
                    if not ((nxt == 0 and curr != 0) or (curr != 3 and nxt == 3 and not h > 0) or (curr == 2 and nxt == 2 and not w < 1)): #or (nxt == 4 and curr != 4)):
                        if (nxt == 1 and x == 0):
                            allowed.append([97, 98])
                        elif (nxt == 1 and x == 0):
                            allowed.append([42, 54])
                        else:
                            allowed.append((y + h, x + w))
            
            mapping[(y,x)] = np.array(allowed)
    
    # y, x
    # print('mapping', mapping[(30, 82)], grid[30][82], grid[30][81])
    tester(mapping, (119, 99), grid)

    with open(path, 'wb') as handle:
        pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)


def tester(mapping, coord, grid):
    ''' coords in y, x (rows, col) '''
    print('Start at ', coord, 'with color ', grid[coord[0]][coord[1]])
    for item in mapping[coord]:
        print('Allowed at ', item, 'with color ', grid[item[0]][item[1]])
            
if __name__ == "__main__":
    name = 'bind100'
    preprocess(getGrid("dbn/" + name + ".png"), "dbn/" + name + ".db")
