#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image, CameraInfo
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import cv2



if __name__ == "__main__":
	bridge = CvBridge()
	rospy.init_node("seadrone_image_node")
	pub_img = rospy.Publisher('/seadrone_image', Image, queue_size = 10)
	pub_info = rospy.Publisher('/seadrone_info', CameraInfo, queue_size = 10)
	#pub_detect = rospy.Publisher('/seadrone_ring_detection', Image, queue_size = 10)
	cap = cv2.VideoCapture('http://192.168.0.122:8090/?action=stream')

	while True:
		ret, frame = cap.read()
		print("Start\n")
		pub_img.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
		'''
		pub_img.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
		cam_info = CameraInfo()
		cam_info.width = 1280
		cam_info.height = 720
		cam_info.K = [3829.436319, 0.000000, 794.572896, 0.000000, 920.751044, 388.229605, 0.0, 0.0, 1.0]
		cam_info.D = [-0.331206 0.072907 -0.016254 -0.025161 0.000000]
		cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
		cam_info.P = [635.284485, 0.000000, 805.929614, 0.000000, 635.284485, 0.000000, 805.929614, 0.000000, 0.0, 0.0, 1.0, 0.0]
		cam_info.distortion_model =  "plumb_bob"
		pub_info.publish(cam_info)
		'''

		'''
		frame = cv2.medianBlur(frame,5)
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