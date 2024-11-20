from library_ST_AM_MB import *

# List of images to scan for faces.
image_array = ["input\\mountain.jpg",
               "input\\mads_mikkelsen.jpg",
               "input\\crowd.jpg",
               "input\\skin.jpg"]

# Calling function for each entry in image_array.
for image in image_array:
    detect_faces(image)
