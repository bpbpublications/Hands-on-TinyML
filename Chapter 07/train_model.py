#! /usr/bin/python

# import the necessary packages
from imutils import paths
import face_recognition
import pickle
import cv2
import os

# our images are located in the dataset folder
print("Getting the data.....")
datapath = list(paths.list_images("dataset"))


# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

print("Processing.....")

# loop over the image paths
for (i, data) in enumerate(datapath):
    name = data.split(os.path.sep)[-2]
    image = cv2.imread(data)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
    boxes = face_recognition.face_locations(rgb, model="hog")

	# compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
    for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
        knownEncodings.append(encoding)
        knownNames.append(name)

# dump the facial encodings + names to disk
print("Dumping in pickle")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
print("Done.....")
