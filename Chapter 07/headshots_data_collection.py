import os
import sys
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import time

name = sys.argv[1] #replace with your name

# get current directory
parent_path = os.getcwd()
path = os.path.join(parent_path+'/dataset', name)
isExist = os.path.exists(path)
print(isExist)
if isExist==False:
    os.mkdir(path)

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
        cv2.imshow("Press Space to take a photo", image)
        rawCapture.truncate(0)
    
        k = cv2.waitKey(1)
        #rawCapture.truncate(0)
        if k%256 == 27: # ESC pressed
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = path+"/sample_{}".format(int(time() * 1000)) + ".jpg"
            #img_name = "image_{}".format(img_counter) + ".jpg"
            cv2.imwrite(img_name, image)
            print("{} written!".format(img_name))
            #img_counter += 1
            
    if k%256 == 27:
        print("Closing...")
        break

cv2.destroyAllWindows()
