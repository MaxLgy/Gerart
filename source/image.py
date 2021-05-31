import cv2
import numpy as np
import math

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('catVid_3.avi')

# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video stream or file")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('lines.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply(grayimg)
        
        trunc = cl1[-250:, 30:-30]
        trunc_origin = frame[-250:, 30:-30]
        edges = cv2.Canny(trunc, 100, 160)
        cdst = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)
        
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                # print(abs(pt1[0] - pt2[0]))
                if abs(pt1[0] - pt2[0]) < abs(pt1[1] - pt2[1]) + 300:
                    cv2.line(trunc_origin, pt1, pt2, (0,0,255), 1, cv2.LINE_AA)
                else:
                    cv2.line(trunc_origin, pt1, pt2, (0,255,0), 1, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Frame',frame)
        cv2.imshow('edges', cdst)
        # cv2.imshow('clahe', cl1)
        #cv2.imshow('trunc img', trunc)

        out.write(frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break

  # Break the loop
    else: 
        break

# When everything done, release the video capture object
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()