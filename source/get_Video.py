import cv2
import numpy as np
import sys

sys.path.insert(1, '../drivers')
import dartv2b_basis as bot


time = int(input("Temps en secondes : "))

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

mybot = bot.DartV2Basis()

compte = 0

while(compte<time*30):
    ret, frame = cap.read()

    if ret == True: 
        
        mybot.set_speed(100,100)
        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame    
        #cv2.imshow('frame',frame)

        # Press Q on keyboard to stop recording
        compte+=1

mybot.set_speed(0,0)
mybot.end()

# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()

