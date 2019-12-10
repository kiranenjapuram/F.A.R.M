#! /usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
import rospy
from std_msgs.msg import Int32


DIR = 12
STEP =5
CW = 1
CCW = 0
EN=7
M0=8
M1=11
M2=25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(M0, GPIO.OUT)
GPIO.setup(M1, GPIO.OUT)
GPIO.setup(M2, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)


delay=0.0005
GPIO.output(M0, GPIO.LOW)
GPIO.output(M1, GPIO.LOW)
GPIO.output(M2, GPIO.LOW)
GPIO.output(EN, GPIO.LOW)

 

def walk():
	rospy.Subscriber('motor_distance',Int32,callback)
	rospy.spin()




def callback(distance):
	rospy.loginfo("starting motor..")
	angle=(360*distance.data)/4.71
	if angle > 0:                                                ##FOR CLOCKWISE DIRECTION
                rospy.loginfo("running motor %d cm forward",distance.data)
		step_count=(angle)/1.8
		rospy.loginfo(int(step_count))		
		for x in range(int(step_count)):
			GPIO.output(EN, GPIO.LOW)
			GPIO.output(DIR, GPIO.HIGH)
			GPIO.output(STEP, GPIO.HIGH)
			sleep(delay)
			GPIO.output(STEP, GPIO.LOW)			
			sleep(delay)
			GPIO.output(EN,GPIO.HIGH)
	 	#sleep(0.005)

	elif angle < 0:                                            ##FOR ANTICLOCKWISE DIRECTION
		angle=(angle)*(-1)
		rospy.loginfo("running motor %d cm backward",distance.data)
		step_count=(angle)/1.8
		rospy.loginfo(int(step_count))
				
		for x in range(int(step_count)):
			 GPIO.output(EN, GPIO.LOW) 
			 GPIO.output(DIR, GPIO.LOW)
			 GPIO.output(STEP, GPIO.HIGH)
			 sleep(delay)
			 GPIO.output(STEP, GPIO.LOW)
			 sleep(delay)
	 		 GPIO.output(EN,GPIO.HIGH)
		#sleep(0.005)
	GPIO.output(EN,GPIO.HIGH)
	

if __name__=='__main__':
	rospy.init_node('run',anonymous=True)
walk()
GPIO.cleanup()
