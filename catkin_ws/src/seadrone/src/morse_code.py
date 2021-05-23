#!/usr/bin/env python

import rospy
import numpy as np
import cv2
import time

from std_msgs.msg import Int16

def morse_code():
    rospy.init_node("morse_code", anonymous=True)
    pub_morse = rospy.Publisher('/seadrone/morse_code', Int16, queue_size = 10)
    rospy.Subscriber("/hand_gesture/number", Int16, predict_cb)
    rate = rospy.Rate(1000) # 1000hz

    rospy.spin()


'''
    while not rospy.is_shutdown():
        morse = input("Please enter a word: ")

        for i in morse:
            # * —
            if i == 'a' or i == 'A':
                short_signal()
                long_signal()

            # — * * *
            elif i == 'b' or i == 'B':
                long_signal()
                short_signal()
                short_signal()
                short_signal()

            # — * — *
            elif i == 'c' or i == 'C':
                long_signal()
                short_signal()
                long_signal()
                short_signal()

            # — * *
            elif i == 'd' or i == 'D':
                long_signal()
                short_signal()
                short_signal()

            # *
            elif i == 'e' or i == 'E':
                short_signal()

            # * * — *
            elif i == 'f' or i == 'F':
                short_signal()
                short_signal()
                long_signal()
                short_signal()

            # — — *
            elif i == 'g' or i == 'G':
                long_signal()
                long_signal()
                short_signal()

            # * * * *
            elif i == 'h' or i == 'H':
                short_signal()
                short_signal()
                short_signal()
                short_signal()

            # * *
            elif i == 'i' or i == 'I':
                short_signal()
                short_signal()

            # * — — —
            elif i == 'j' or i == 'J':
                short_signal()
                long_signal()
                long_signal()
                long_signal()

            # — * —
            elif i == 'k' or i == 'K':
                long_signal()
                short_signal()
                long_signal()
                
            # * — * *
            elif i == 'l' or i == 'L':
                short_signal()
                long_signal()
                short_signal()
                short_signal()

            # — —
            elif i == 'm' or i == 'M':
                long_signal()
                long_signal()

            # — *
            elif i == 'n' or i == 'N':
                long_signal()
                short_signal()

            # — — —
            elif i == 'o' or i == 'O':
                long_signal()
                long_signal()
                long_signal()

            # * — — *
            elif i == 'p' or i == 'P':
                short_signal()
                long_signal()
                long_signal()
                short_signal()

            # — — * —
            elif i == 'q' or i == 'Q':
                long_signal()
                long_signal()
                short_signal()
                long_signal()

            # * — *
            elif i == 'r' or i == 'R':
                short_signal()
                long_signal()
                short_signal()

            # * * *
            elif i == 's' or i == 'S':
                short_signal()
                short_signal()
                short_signal()

            # —
            elif i == 't' or i == 'T':
                long_signal()

            # * * —
            elif i == 'u' or i == 'U':
                short_signal()
                short_signal()
                long_signal()

            # * * * —
            elif i == 'v' or i == 'V':
                short_signal()
                short_signal()
                short_signal()
                long_signal()

            # * — —
            elif i == 'w' or i == 'W':
                short_signal()
                long_signal()
                long_signal()

            # — * * —
            elif i == 'x' or i == 'X':
                long_signal()
                short_signal()
                short_signal()
                long_signal()

            # — * — —
            elif i == 'y' or i == 'Y':
                long_signal()
                short_signal()
                long_signal()
                long_signal()

            # — — * *
            elif i == 'z' or i == 'Z':
                long_signal()
                long_signal()
                short_signal()
                short_signal()

            # * — — — —
            elif i == '1':
                short_signal()
                long_signal()
                long_signal()
                long_signal()
                long_signal()
            
            # * * — — —
            elif i == '2':
                short_signal()
                short_signal()
                long_signal()
                long_signal()
                long_signal()

            # * * * — —
            elif i == '3':
                short_signal()
                short_signal()
                short_signal()
                long_signal()
                long_signal()

            # * * * * —
            elif i == '4':
                short_signal()
                short_signal()
                short_signal()
                short_signal()
                long_signal()

            # * * * * *
            elif i == '5':
                short_signal()
                short_signal()
                short_signal()
                short_signal()
                short_signal()

            # — * * * *
            elif i == '6':
                long_signal()
                short_signal()
                short_signal()
                short_signal()
                short_signal()

            # — — * * *
            elif i == '7':
                long_signal()
                long_signal()
                short_signal()
                short_signal()
                short_signal()

            # — — — * *
            elif i == '8':
                long_signal()
                long_signal()
                long_signal()
                short_signal()
                short_signal()

            # — — — — *
            elif i == '9':
                long_signal()
                long_signal()
                long_signal()
                long_signal()
                short_signal()

            # — — — — —
            elif i == '0':
                long_signal()
                long_signal()
                long_signal()
                long_signal()
                long_signal()
                
            else:
                print("Done!!!\n")

            time.sleep(2)

        rate.sleep()
'''

def predict_cb(data):
    i = data.data
    print(i)
    # * — — — —
    if i == 1:
        short_signal()
        long_signal()
        long_signal()
        long_signal()
        long_signal()
    
    # * * — — —
    elif i == 2:
        short_signal()
        short_signal()
        long_signal()
        long_signal()
        long_signal()

    # * * * — —
    elif i == 3:
        short_signal()
        short_signal()
        short_signal()
        long_signal()
        long_signal()

    # * * * * —
    elif i == 4:
        short_signal()
        short_signal()
        short_signal()
        short_signal()
        long_signal()

    # * * * * *
    elif i == 5:
        short_signal()
        short_signal()
        short_signal()
        short_signal()
        short_signal()

    # — * * * *
    elif i == 6:
        long_signal()
        short_signal()
        short_signal()
        short_signal()
        short_signal()

    # — — * * *
    elif i == 7:
        long_signal()
        long_signal()
        short_signal()
        short_signal()
        short_signal()

    # — — — * *
    elif i == 8:
        long_signal()
        long_signal()
        long_signal()
        short_signal()
        short_signal()

    # — — — — *
    elif i == 9:
        long_signal()
        long_signal()
        long_signal()
        long_signal()
        short_signal()

    # — — — — —
    elif i == 0:
        long_signal()
        long_signal()
        long_signal()
        long_signal()
        long_signal()
        
    else:
        print("Done!!!\n")

    time.sleep(5)


def short_signal():
    pub_morse = rospy.Publisher('/seadrone/morse_code', Int16, queue_size = 10)
    rate = rospy.Rate(1000) # 1000hz
    joy_node = 1
    pub_morse.publish(joy_node)
    time.sleep(0.5)
    joy_node = 0
    pub_morse.publish(joy_node)
    time.sleep(1)

def long_signal():
    pub_morse = rospy.Publisher('/seadrone/morse_code', Int16, queue_size = 10)
    rate = rospy.Rate(1000) # 1000hz
    joy_node = 1
    pub_morse.publish(joy_node)
    time.sleep(1.5)
    joy_node = 0
    pub_morse.publish(joy_node)
    time.sleep(1)

if __name__ == "__main__":
    try:
        morse_code()
    except rospy.ROSInterruptException:
        pass

