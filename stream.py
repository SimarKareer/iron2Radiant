import time
import streamlink
import util
import matplotlib.pyplot as plt
import cv2
import numpy as np

# use live streamer to figure out the stream info
def stream(ping):
    streams = streamlink.streams("http://www.twitch.tv/Galaxspheria")
    stream = streams['best']
    vid = cv2.VideoCapture(stream.url)
    ret, frame = vid.read()
    count = 20
    while ret:
        ret, frame = vid.read()
        if count % 20 == 0:
            map_img = util.imgToMap(np.array(frame))
            locs = util.imToObs(map_img, None, 15, vis=True)
            ping(locs)
            print(type(ping))
        count += 1
# open our out file. 
#fname = "test.mpg"
#vid_file = open(fname,"wb")
# dump from the stream into an mpg file -- get a buffer going
#fd = stream.open()
#for i in range(0,2*2048):
#    if i%256==0:
#        print("Buffering...")
#    new_bytes = fd.read(1024)
#vid_file.write(new_bytes)
# open the video file from the begining
#print("Done buffering.")
