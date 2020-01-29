#!/usr/bin/env python

from pyzbar import pyzbar
import cv2
import sys
from pyzbar import pyzbar
import argparse

import numpy as np
#import subprocess
import cv2

import rospy

from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo

#import camera_info_manager
from std_msgs.msg import Float64
from cv_bridge import CvBridge, CvBridgeError


import cv2

cap=cv2.VideoCapture(0)
ErrorImage=cv2.imread('ImageNotFound.png',1)
face_cascade = cv2.CascadeClassifier('/home/agribot/Desktop/QRlocalization/QR_Localizatoin/haarcascade_frontalface_default.xml')

def p_publisher():
		#rospy.init_node('image_converter', anonymous=True)
		rospy.init_node('distance', anonymous=True)
		
		#image_pub = rospy.Publisher("image_topic_2",Image)
		distance_pub = rospy.Publisher("distance_topic_2",Float64,queue_size=10)
		 
		bridge = CvBridge()
		while True:
			ref,img=cap.read(0)
			#cv2.moments(img)
			#cv2.putText(img,'bot_position=0,0',(0,0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

			if ref:
				# adding variables for localization calculation
				Localization_variable = ()
				NumQRtags = 0
				Object_variable = ()
				NumObjects = 0


				# getting the QR objects from image
				barcodes=pyzbar.decode(img)
				for barcode in barcodes:
					    NumQRtags += 1
					    (x, y, w, h) = barcode.rect
						 	#cv2.putText(img,'bot_position=0,0',(0,0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
					    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
					    barcodeData = barcode.data.decode()
					    barcodeType = barcode.type
					    Location = (round((x + w/2) ), round((y + h/2)))
					    QRobject = Location + (int(barcodeData),)
					    Localization_variable = Localization_variable + (QRobject,)
					    #text = "{} ({})".format(barcodeData, barcodeType)
					    text = "{} cm".format(barcodeData)
					    cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				Localization_variable = (NumQRtags,) + Localization_variable
			#a=x+w/2
			#b=y+h/2
				#cv2.putText(img,'bot_position=0,0',(a,b), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				# decoding the faces
				gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				M=cv2.moments(gray)
				cX=int(M["m10"]/M["m00"])
				cY=int(M["m01"]/M["m00"])
				Center=img.shape
				cX=int(Center[1]/2)
				#print(Center[0]/2)
				print(cX)
				cv2.putText(img,'.',(cX,cY),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
				faces = face_cascade.detectMultiScale(gray, 1.1, 10)
				for (x, y, w, h) in faces:
				    NumObjects += 1
				    Location = (round((x + w/2)), round((y + h/2)))
				    Object_variable = Object_variable + (Location,)
				    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
				    text = "Face"
				    #cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


				Object_variable = (NumObjects,) + Object_variable

				# checking num of QR and selecting the technique

				if NumQRtags==1:
					# only one QR tag detected
					print("1 QR tag detected not enough. Find more QR tag")
				else:
					if NumQRtags==2:

						# calculating object distance assuming only two QR tags are in image
						QR_left_location = Localization_variable[1][0]
						QR_Right_location = Localization_variable[2][0]
						QR_left_distance = Localization_variable[1][2]
						QR_Right_distance = Localization_variable[2][2]
						#print(QR_left_distance)
						#print(QR_Right_distance)
						Object_location = cX
						Object_distance = ((Object_location - QR_Right_location) * (QR_left_distance - QR_Right_distance) / (
						QR_left_location - QR_Right_location)) + QR_Right_distance
						Object_distance=round(Object_distance,2)
						#print(Object_distance)
						text=str(Object_distance)+ " cm"
						#distance_pub.publish(Object_distance)
						print(text)


						current_distance=float(Object_distance)
						
				                destination_distance=input("enter the destination distance for motor=")
				                if current_distance < destination_distance :
				    	         difference=destination_distance - current_distance

					        elif current_distance > destination_distance :
						
					         difference=current_distance-destination_distance
						 difference=(-difference)
						distance_pub.publish(difference)
						rospy.loginfo("difference is %f ",difference)

						#cv2.putText(img,text, (int(Center[1]/2),int(Center[0]/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
					else:
						print("more than 2 QR tags in system")
				# displaying video feed
				cv2.imshow("Video Feed",img)
                               # image_pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
				# checking for exit key
				KeyPressed = cv2.waitKey(10)
				if KeyPressed ==ord('q'):
					break
			else:
				# if image not found pop up error message
				cv2.imshow("Video Feed",ErrorImage)


if __name__=='__main__':
    try:
        p_publisher()
    except rospy.ROSInterruptException:
        pass
