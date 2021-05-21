#!/usr/bin/env python
# https://maker.pro/raspberry-pi/projects/raspberry-pi-webcam-robot
# https://osoyoo.com/2020/04/30/install-a-web-camera-on-raspberry-pi/


import rospy
import numpy as np
import cv2

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import String

def image():
	bridge = CvBridge()
	rospy.init_node("seadrone_image_node", anonymous=True)
	pub_img = rospy.Publisher('/seadrone_image/image', Image, queue_size = 10)
	pub_info = rospy.Publisher('/seadrone_info', CameraInfo, queue_size = 10)
	cap = cv2.VideoCapture('http://192.168.0.122:8090/?action=stream')
	rate = rospy.Rate(1000) # 1000hz
	print("Start\n")

	while not rospy.is_shutdown():
		ret, frame = cap.read()
		cam_info = CameraInfo()
		cam_info.width = 1280
		cam_info.height = 720
		cam_info.K = [3829.436319, 0.000000, 794.572896, 0.000000, 920.751044, 388.229605, 0.0, 0.0, 1.0]
		cam_info.D = [-0.331206, 0.072907, -0.016254, -0.025161, 0.000000]
		cam_info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
		cam_info.P = [635.284485, 0.000000, 805.929614, 0.000000, 635.284485, 0.000000, 805.929614, 0.000000, 0.0, 0.0, 1.0, 0.0]
		cam_info.distortion_model = "plumb_bob"
		pub_info.publish(cam_info)
		pub_img.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
		rate.sleep()

if __name__ == "__main__":
	try:
		image()
	except rospy.ROSInterruptException:
		pass


