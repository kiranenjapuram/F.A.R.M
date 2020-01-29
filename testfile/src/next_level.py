#! /usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
import rospy
import numpy
#import os
from std_msgs.msg import Float64
#import subprocess #go to the end of callback function

DIR = 12
STEP =5
CW = 1
CCW = 0
EN=8
#M0=8
#M1=11
#M2=25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN, GPIO.OUT)
#GPIO.setup(M0, GPIO.OUT)
#GPIO.setup(M1, GPIO.OUT)
#GPIO.setup(M2, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)


delay=0.0005
#GPIO.output(M0, GPIO.LOW)
#GPIO.output(M1, GPIO.LOW)
#GPIO.output(M2, GPIO.LOW)
GPIO.output(EN, GPIO.LOW)

 

def walk():
	rospy.Subscriber('distance_topic_2',Float64,callback)
	rospy.spin()




def callback(difference):
	
	rospy.loginfo("starting motor..")
	angle=(360*difference.data)/34
	if angle > 0:                                                ##FOR CLOCKWISE DIRECTION
                rospy.loginfo("running motor %f cm forward",difference.data)
		step_count=(angle)/1.8
		rospy.loginfo(step_count)		
		for x in numpy.arange((step_count)):
			GPIO.output(EN, GPIO.LOW)
			GPIO.output(DIR, GPIO.HIGH)
			GPIO.output(STEP, GPIO.HIGH)
			sleep(delay)
			GPIO.output(STEP, GPIO.LOW)			
			sleep(delay)
			GPIO.output(EN,GPIO.HIGH)
	 	#sleep(0.005)
		#rospy.loginfo("moving right side towards destination",difference.data)

	elif angle < 0:                                            ##FOR ANTICLOCKWISE DIRECTION
		angle=(angle)*(-1)
		rospy.loginfo("running motor %f cm BACKWARD",difference.data)
		step_count=(angle)/1.8
		rospy.loginfo(step_count)
				
		for x in numpy.arange((step_count)):
			 GPIO.output(EN, GPIO.LOW) 
			 GPIO.output(DIR, GPIO.LOW)
			 GPIO.output(STEP, GPIO.HIGH)
			 sleep(delay)
			 GPIO.output(STEP, GPIO.LOW)
			 sleep(delay)
	 		 GPIO.output(EN,GPIO.HIGH)
		#sleep(0.005)
		#rospy.loginfo("moving left side towards destination",difference.data) 
	GPIO.output(EN,GPIO.HIGH)
	flag=1
	
	#os.system('python servo.py') 
	#subprocess.call(["python","servo1.py"])	#used to execute terminal commands in python file

if __name__=='__main__':
	rospy.init_node('run',anonymous=True)
walk()
GPIO.cleanup()

