from heatmap import generateMap
from stream import stream
from dbn.Game import Game
from flask import Response
from flask import Flask
from flask import render_template
from scipy import ndimage
import numpy as np
import threading
import argparse
import datetime
import time
import io

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")

def detect_motion(game):
    # grab global references to the video stream, output frame, and
    # lock variables
    global outputFrame, lock
    # initialize the total number of frames read thus far

    i = 0

    # loop over frames from the video stream
    while True:
        # x = np.zeros((100, 100))
        # x[50, i] = 1
        heatmap_data = g.getBeliefDist() #ndimage.filters.gaussian_filter(x, sigma=16)

        hardCodeAgent = None
        for name, heatmap in heatmap_data:
            if name == "sage":
                hardCodeAgent = heatmap

        print(hardCodeAgent)

        frame, buffer = generateMap(hardCodeAgent)
        
        i += 2
        if (i > 99):
            i = 0

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()
            frame.close()
            buffer.close()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        time.sleep(0.1)
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            with io.BytesIO() as output:
                outputFrame.save(output, format="JPEG")
                encodedImage = output.getvalue()
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
    numParticles = 100
    g = Game('./dbn/bind100.png', numParticles, ['omen', 'sage'])
    t = threading.Thread(target=detect_motion, args=[g])
    t.daemon = True
    t.start()
    s = threading.Thread(target=stream, args=[g.tick])
    s.daemon = True
    s.start()
    # start the flask app
    app.run(port=3000, debug=True,
        threaded=True, use_reloader=False)

