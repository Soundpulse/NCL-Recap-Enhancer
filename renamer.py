import os

currentPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
videosPath = currentPath + "/processed/"

for file in os.listdir(videosPath):
	if file.endswith(".srt"):
		name = os.path.splitext(file)[0]
		name = name + "-converted.srt"
		
		os.rename(videosPath + file, videosPath + name)
		