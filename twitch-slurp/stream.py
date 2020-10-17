import time
import streamlink

# use live streamer to figure out the stream info
streams = streamlink.streams("http://www.twitch.tv/valorant_korea")
stream = streams['best']
# open our out file. 
fname = "test.mpg"
vid_file = open(fname,"wb")
# dump from the stream into an mpg file -- get a buffer going
fd = stream.open()
for i in range(0,2*2048):
    if i%256==0:
        print("Buffering...")
    new_bytes = fd.read(1024)
    vid_file.write(new_bytes)
# open the video file from the begining
print("Done buffering.")
