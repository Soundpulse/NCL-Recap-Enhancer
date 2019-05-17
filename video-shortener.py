import os
import sys
import time

currentPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
videosPath = currentPath + "/subbed_vids/"

# CHANGE ME!
SOUNDED_SPEED = "2"
SLIENT_SPEED = "8"
FRAME_MARGIN = "2"

for file in os.listdir(videosPath):
    if file.endswith(".mp4"):
        video_name = os.path.splitext(file)[0]

        os.system(
        "python jumpcutter.py --input_file " + video_name + ".mp4" + " --output_file " + "SHORTENED_" + video_name + ".mp4" + " --sounded_speed " + SOUNDED_SPEED + " --slient_speed " + SLIENT_SPEED + " --frame_margin " + FRAME_MARGIN
        )