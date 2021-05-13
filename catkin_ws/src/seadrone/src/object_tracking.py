#!/usr/bin/env python
import rospy
import numpy as np
import cv2
import imutils
import time
import argparse

from collections import deque
from imutils.video import VideoStream
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())


bridge = CvBridge()
rospy.init_node("seadrone_image_node")
pub_img = rospy.Publisher('/seadrone_image/image', Image, queue_size = 10)
pub_info = rospy.Publisher('/seadrone_info', CameraInfo, queue_size = 10)
cap = cv2.VideoCapture('http://192.168.0.122:8090/?action=stream')


# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#greenLower = (10, 80, 0)
#greenUpper = (90, 255, 255)
#greenLower = (120, 150, 120)  #red
#greenUpper = (255, 255, 255)
greenLower = (80, 155, 120)  #blue
greenUpper = (120, 255, 255)

counter = 0
(dX, dY) = (0, 0)
direction = ""
pts = deque(maxlen=args["buffer"])

time.sleep(2.0)

# keep looping
while not rospy.is_shutdown():
	# grab the current frame
	ret, frame = cap.read()
	pub_img.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			# https://blog.gtwang.org/programming/opencv-drawing-functions-tutorial/
			# https://vimsky.com/zh-tw/examples/usage/python-opencv-cv2-circle-method.html
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			# update the points queue
			pts.appendleft(center)

	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
			# ensure there is significant movement in the
			# x-direction
			if np.abs(dX) > 20:
				dirX = "East" if np.sign(dX) == 1 else "West"
			# ensure there is significant movement in the
			# y-direction
			if np.abs(dY) > 20:
				dirY = "North" if np.sign(dY) == 1 else "South"
			# handle when both directions are non-empty
			if dirX != "" and dirY != "":
				direction = "{}-{}".format(dirY, dirX)
			# otherwise, only one direction is non-empty
			else:
				direction = dirX if dirX != "" else dirY

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the movement deltas and the direction of movement on
	# the frame
	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	counter += 1
	
	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord('q'):
 		break

# close all windows
cv2.destroyAllWindows()




		