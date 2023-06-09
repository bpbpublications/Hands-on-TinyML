from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

from picamera import PiCamera
from picamera.array import PiRGBArray

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection

print("Activating the camera.....")
data = pickle.loads(open(encodingsP, "rb").read())

cam = PiCamera()
#cam.resolution = (512, 304)
cam.resolution = (320, 240)
cam.framerate = 10
#rawCapture = PiRGBArray(cam, size=(512, 304))
rawCapture = PiRGBArray(cam, cam.resolution)

#img_counter = 0

while True:
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        rawCapture.truncate(0)
        #k = cv2.waitKey(1)
        #rawCapture.truncate(0)        
        k = cv2.waitKey(1) & 0xFF
        #rawCapture.truncate(0)
    
        if k%256 == 27: # ESC pressed
            break
        boxes = face_recognition.face_locations(image)
	    # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(image, boxes)
        names = []
        
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown" #if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                #If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    print(currentname)

            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(image, (left, top), (right, bottom),
                (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                .8, (0, 255, 255), 2)
        
        cv2.imshow("window", image)

            
    if k%256 ==27 : # ESC pressed
        print("Closing...")
        break            


cv2.destroyAllWindows()