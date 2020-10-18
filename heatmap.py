import matplotlib
import seaborn as sns
import io
import numpy as np
import base64
from scipy import ndimage
from PIL import Image

def generateMap(data):
    wd = matplotlib.cm.winter._segmentdata # only has r,g,b  
    wd['alpha'] =  ((0.0, 0.0, 0.3), 
                (0.3, 0.3, 1.0),
                (1.0, 1.0, 1.0))

    # get the map image as an array so we can plot it 
    map_img = matplotlib.image.imread('rsz_map.png') 

    sns.set()
    matplotlib.pyplot.figure(figsize=(10,10))
    hmax = sns.heatmap(data,
                cmap = matplotlib.cm.winter,
                alpha = 0.3, # whole heatmap is translucent
                zorder = 2,
                cbar = False,
                linewidths = 0.0,
            )

    hmax.set(xticklabels=[])
    hmax.set(yticklabels=[])
    sns.despine(top=True, right=True, left=True, bottom=True)

    # heatmap uses pcolormesh instead of imshow, so we can't pass through 
    # extent as a kwarg, so we can't mmatch the heatmap to the map. Instead, 
    # match the map to the heatmap:

    hmax.imshow(map_img,
            aspect = hmax.get_aspect(),
            extent = hmax.get_xlim() + hmax.get_ylim(),
            zorder = 1) #put the map under the heatmap

    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='jpeg')
    matplotlib.pyplot.close()
    buf.seek(0)

    im = Image.open(buf)
    return im, buf

def mapLoop():
    # create heat map
    for i in range(0, 1):
        x = np.zeros((100, 100))
        x[50, i] = 1
        heatmap_data = ndimage.filters.gaussian_filter(x, sigma=16)
        url = generateMap(heatmap_data)
        print(url)
        print('loop ' + str(i), end="\r")

# mapLoop()
