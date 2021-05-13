#!/usr/bin/env python
import rospy
import numpy as np
import cv2
import time
import argparse
import imutils

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CameraInfo
from collections import deque



if __name__ == "__main__":
	bridge = CvBridge()
	rospy.init_node("seadrone_image_node")
	pub_img = rospy.Publisher('/seadrone_image/image', Image, queue_size = 10)
	pub_info = rospy.Publisher('/seadrone_info', CameraInfo, queue_size = 10)
	cap = cv2.VideoCapture('http://192.168.0.122:8090/?action=stream')
	font = cv2.FONT_HERSHEY_COMPLEX
	
	pub_red = rospy.Publisher('/seadrone_image/detect_red', Image, queue_size = 10)
	pub_blue = rospy.Publisher('/seadrone_image/detect_blue', Image, queue_size = 10)
	pub_green = rospy.Publisher('/seadrone_image/detect_green', Image, queue_size = 10)
	pub_detect = rospy.Publisher('/seadrone_image/detect_result', Image, queue_size = 10)
	#pub_detect = rospy.Publisher('/seadrone_ring_detection', Image, queue_size = 10)


	def nothing(x):
		pass

	#Trackbars
	cv2.namedWindow("Camera")
	cv2.createTrackbar("swith_code", "Camera", 0, 1, nothing)
	
	#red
	cv2.createTrackbar("R_LH", "Camera", 0, 255, nothing)
	cv2.createTrackbar("R_LS", "Camera", 0, 255, nothing)
	cv2.createTrackbar("R_LV", "Camera", 0, 255, nothing)
	cv2.createTrackbar("R_UH", "Camera", 0, 255, nothing)
	cv2.createTrackbar("R_US", "Camera", 0, 255, nothing)
	cv2.createTrackbar("R_UV", "Camera", 0, 255, nothing)
	'''
	#green
	cv2.createTrackbar("G_LH", "Camera", 0, 255, nothing)
	cv2.createTrackbar("G_LS", "Camera", 0, 255, nothing)
	cv2.createTrackbar("G_LV", "Camera", 0, 255, nothing)
	cv2.createTrackbar("G_UH", "Camera", 0, 255, nothing)
	cv2.createTrackbar("G_US", "Camera", 0, 255, nothing)
	cv2.createTrackbar("G_UV", "Camera", 0, 255, nothing)
	#blue
	cv2.createTrackbar("B_LH", "Camera", 0, 255, nothing)
	cv2.createTrackbar("B_LS", "Camera", 0, 255, nothing)
	cv2.createTrackbar("B_LV", "Camera", 0, 255, nothing)
	cv2.createTrackbar("B_UH", "Camera", 0, 255, nothing)
	cv2.createTrackbar("B_US", "Camera", 0, 255, nothing)
	cv2.createTrackbar("B_UV", "Camera", 0, 255, nothing)
	'''
	#swith input
	cv2.setTrackbarPos('swith_code', "Camera", 1)
	
	#red color
	cv2.setTrackbarPos('R_LH', "Camera", 120)
	cv2.setTrackbarPos('R_LS', "Camera", 150)
	cv2.setTrackbarPos('R_LV', "Camera", 120)
	cv2.setTrackbarPos('R_UH', "Camera", 255)
	cv2.setTrackbarPos('R_US', "Camera", 255)
	cv2.setTrackbarPos('R_UV', "Camera", 255)
	'''
	#green color
	cv2.setTrackbarPos('G_LH', "Camera", 52)
	cv2.setTrackbarPos('G_LS', "Camera", 135)
	cv2.setTrackbarPos('G_LV', "Camera", 55)
	cv2.setTrackbarPos('G_UH', "Camera", 85)
	cv2.setTrackbarPos('G_US', "Camera", 255)
	cv2.setTrackbarPos('G_UV', "Camera", 255)
	
	#blue color
	cv2.setTrackbarPos('B_LH', "Camera", 89)
	cv2.setTrackbarPos('B_LS', "Camera", 127)
	cv2.setTrackbarPos('B_LV', "Camera", 61)
	cv2.setTrackbarPos('B_UH', "Camera", 168)
	cv2.setTrackbarPos('B_US', "Camera", 255)
	cv2.setTrackbarPos('B_UV', "Camera", 255)
	'''
	#swith output
	swith_code = cv2.getTrackbarPos("swith_code", "Camera")

	#Detection
	while True:
		#swith_code = cv2.getTrackbarPos("swith_code", "Camera")
		ret, frame = cap.read()

		cam_info = CameraInfo()
		cam_info.width = 1280
		cam_info.height = 720

		cam_info.K = [3829.436319, 0.000000, 794.572896, 0.000000, 920.751044, 388.229605, 0.0, 0.0, 1.0]
		cam_info.D = [-0.331206, 0.072907, -0.016254, -0.025161, 0.000000]
		cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
		cam_info.P = [635.284485, 0.000000, 805.929614, 0.000000, 635.284485, 0.000000, 805.929614, 0.000000, 0.0, 0.0, 1.0, 0.0]

		cam_info.distortion_model =  "plumb_bob"
		pub_info.publish(cam_info)
		pub_img.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
		frame = cv2.medianBlur(frame, 13)

		'''
		circles = cv2.HoughCircles(frame,cv2.HOUGH_GRADIENT,1,20,
							param1=50,param2=30,minRadius=0,maxRadius=0)
		circles = np.uint16(np.around(circles)
		for i in circles[0,:]:
			# draw the outer circle
			cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle
			cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
		pub_detect.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
		'''

		image = frame
		blurred_image = cv2.GaussianBlur(image, (11, 11), 0)
		hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

		# detect red
		
		R_LH = cv2.getTrackbarPos("R_LH", "Camera")
		R_LS = cv2.getTrackbarPos("R_LS", "Camera")
		R_LV = cv2.getTrackbarPos("R_LV", "Camera")
		R_UH = cv2.getTrackbarPos("R_UH", "Camera")	
		R_US = cv2.getTrackbarPos("R_US", "Camera")
		R_UV = cv2.getTrackbarPos("R_UV", "Camera")
		lower_red = np.array([R_LH, R_LS, R_LV])
		upper_red = np.array([R_UH, R_US, R_UV])
		
		#lower_red = np.array([120, 150, 120])
		#upper_red = np.array([255, 255, 255])
		#lower_red = np.array([0, 50, 50])
		#upper_red = np.array([180, 255, 255])
		mask_red = cv2.inRange(hsv, lower_red, upper_red)
	
		# detect green
		'''
		G_LH = cv2.getTrackbarPos("G_LH", "Camera")
		G_LS = cv2.getTrackbarPos("G_LS", "Camera")
		G_LV = cv2.getTrackbarPos("G_LV", "Camera")
		G_UH = cv2.getTrackbarPos("G_UH", "Camera")	
		G_US = cv2.getTrackbarPos("G_US", "Camera")
		G_UV = cv2.getTrackbarPos("G_UV", "Camera")
		lower_green = np.array([G_LH, G_LS, G_LV])
		upper_green = np.array([G_UH, G_US, G_UV])
		'''
		#lower_green = np.array([52, 135, 55])
		#upper_green = np.array([85, 255, 255])
		lower_green = np.array([10, 80, 0])
		upper_green = np.array([90, 255, 255])
		mask_green = cv2.inRange(hsv, lower_green, upper_green)

		# detect blue
		'''
		B_LH = cv2.getTrackbarPos("B_LH", "Camera")
		B_LS = cv2.getTrackbarPos("B_LS", "Camera")
		B_LV = cv2.getTrackbarPos("B_LV", "Camera")
		B_UH = cv2.getTrackbarPos("B_UH", "Camera")	
		B_US = cv2.getTrackbarPos("B_US", "Camera")
		B_UV = cv2.getTrackbarPos("B_UV", "Camera")
		lower_blue = np.array([B_LH, B_LS, B_LV])
		upper_blue = np.array([B_UH, B_US, B_UV])
		'''
		lower_blue = np.array([80, 155, 120])
		upper_blue = np.array([120, 255, 255])
		mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
	
		mask = mask_red + mask_green + mask_blue
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		red = cv2.bitwise_and (image, image, mask=mask_red)
		green = cv2.bitwise_and (image, image, mask=mask_green)
		blue = cv2.bitwise_and (image, image, mask=mask_blue)
		result = cv2.bitwise_and (image, image, mask=mask)
		
		# https://blog.csdn.net/sunny2038/article/details/12889059
		#_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)

		if len(contours) > 0:
			contour = max(contours, key=cv2.contourArea)
			M = cv2.moments(contour)
			area = cv2.contourArea(contour)
			if area > 100:
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				peri = cv2.arcLength(contour, True)
				approx = cv2.approxPolyDP(contour, 0.03*peri, True)

				if len (approx) == 3:
					shape = "Triangle"
				elif len (approx) == 4:
					shape = "Rectangle"
				elif 6 <= len (approx) <= 8:
					shape = "Circle"
				else:
					shape = "not detect shape"

				c = image[cy][cx]
				if c[0] > c[1] and c[0] > c[2] and c[0] > 100:
					color = "Blue"
				elif c[1] > c[0] and c[1] > c[2] and c[1] > 80:
					color = "Green"
				elif c[2] > c[0] and c[2] > c[1] and c[2] > 100:
					color = "Red"
				else:
					color = "not detect color"

				(x, y, w, h) = cv2.boundingRect(approx)
				cv2.rectangle(result, (cx, cy), (x+w, y+h), (0 , 255, 0), 4)
				cv2.rectangle(image, (cx, cy), (x+w, y+h), (0 , 255, 0), 4)

				if shape == "not detect shape" or color == "not detect color":
					pub_red.publish(bridge.cv2_to_imgmsg(red, "bgr8"))
					pub_green.publish(bridge.cv2_to_imgmsg(green, "bgr8"))
					pub_blue.publish(bridge.cv2_to_imgmsg(blue, "bgr8"))
					pub_detect.publish(bridge.cv2_to_imgmsg(result, "bgr8"))
				else:
					#cv2.drawContours(result, contour, -1, (0, 255, 0), 3)
					#cv2.drawContours(image, contour, -1, (0, 255, 0), 3)
					text = "{} / {} / {} / {}".format(cx, cy, color, shape)			
					cv2.putText(result, text, (cx, cy), font, 1.5, (255, 255, 255), 2)

					pub_red.publish(bridge.cv2_to_imgmsg(red, "bgr8"))
					pub_green.publish(bridge.cv2_to_imgmsg(green, "bgr8"))
					pub_blue.publish(bridge.cv2_to_imgmsg(blue, "bgr8"))
					pub_detect.publish(bridge.cv2_to_imgmsg(result, "bgr8"))

				#cv2.imshow("frame", image)
				#cv2.imshow("mask", mask)
				#cv2.imshow("mask_red", red)
				#cv2.imshow("mask_green", green)
				#cv2.imshow("mask_blue", blue)
				#cv2.imshow("result", result)

		key = cv2.waitKey(1) & 0xFF

	cv2.destroyAllWindows()