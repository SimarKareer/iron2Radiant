import util

map_img = util.imgToMap('test_inputs/omen3.png')
locs = util.imToObs(map_img, None, 12, vis=True)
print(locs)
