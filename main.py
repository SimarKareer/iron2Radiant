import util

map_img = util.imgToMap('test_inputs/killjoy2.png', streamMode=False)
locs = util.imToObs(map_img, None, 12, vis=True)
print(locs)
