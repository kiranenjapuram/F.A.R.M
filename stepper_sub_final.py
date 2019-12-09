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

 

def run():
	rospy.Subscriber('motor_topic',Int32,callback)
	rospy.spin()




def callback(angle):
	rospy.loginfo("starting motor..")

	if angle.data > 0:                                                ##FOR CLOCKWISE DIRECTION
                rospy.loginfo("rotating motor %d clockwise",angle.data)
		step_count=(angle.data)/1.8
		rospy.loginfo(round(step_count))
		step_count=round(step_count)
		step_count=(int(step_count))
		rospy.loginfo(step_count)
		#step_count=step_count*2		
		for x in range(int(step_count)):
			GPIO.output(EN, GPIO.LOW)
			GPIO.output(DIR, GPIO.LOW)
			GPIO.output(STEP, GPIO.HIGH)
			sleep(delay)
			GPIO.output(STEP, GPIO.LOW)			
			sleep(delay)
			GPIO.output(EN,GPIO.HIGH)
	 	sleep(0.005)

	elif angle.data < 0:                                            ##FOR ANTICLOCKWISE DIRECTION
		angle.data=(angle.data)*(-1)
		rospy.loginfo("rotating motor %d anticlockwise",angle.data)
		a_step_count=(angle.data)/1.8
		rospy.loginfo(int(a_step_count))
		a_step_count=round(a_step_count)
		a_step_count=int(a_step_count)
		#a_step_count=a_step_count*2
		rospy.loginfo(int(a_step_count))
		for x in range(int(a_step_count)):
			 GPIO.output(EN, GPIO.LOW) 
			 GPIO.output(DIR, GPIO.HIGH)
			 GPIO.output(STEP, GPIO.HIGH)
			 sleep(delay)
			 GPIO.output(STEP, GPIO.LOW)
			 sleep(delay)
	 		 GPIO.output(EN,GPIO.HIGH)
		sleep(0.005)
	GPIO.output(EN,GPIO.HIGH)
	

if __name__=='__main__':
	rospy.init_node('run',anonymous=True)
run()
GPIO.cleanup()


