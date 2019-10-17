import os
import sys
import time

currentPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
videosPath = currentPath + "/raw_vids/"

# CHANGE ME!
SOUNDED_SPEED = "2"
SLIENT_SPEED = "8"
FRAME_MARGIN = "2"

for file in os.listdir(videosPath):
    if file.endswith(".mp4"):
        video_name = os.path.splitext(file)[0]
		
        os.system(
        "%cd%/bin/Python27/python.exe " +
		"%cd%/bin/Python27/Scripts/autosub_app.py -S en -D en " 
		+ videosPath + video_name + ".mp4"
        )