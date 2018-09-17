from bluetooth import *
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import picamera
import datetime
import time
import threading
import logging

# Initialize Camera
camera = picamera.PiCamera()
camera.resolution = (1280, 720)

# Initialize Bluetooth Socket
server_socket = BluetoothSocket(RFCOMM)

# Setup Bluetooth Server
port = 1
server_socket.bind(("",port))
server_socket.listen(1)

# BT UUID
uuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"

# Start advertised bluetooth service
advertise_service( server_socket, "RSV",
									 service_id = uuid,
									 service_classes = [ uuid, SERIAL_PORT_CLASS ],
									 profiles = [ SERIAL_PORT_PROFILE ] 
										)

threads = []

def vidworker():
	""" thread worker function for video capture """
	camera.start_recording('bt-activated-video.h264.mp4')
	camera.wait_recording(960)
	camera.stop_recording()
	camera.close()
	client_socket.send("Finished Recording Video")
	return 
 
client_socket,address = server_socket.accept()
print("Accepted connection from ", address)

try:
	while 1:
		data = client_socket.recv(1024)
		print("Received: %s" % data)

		if (data == "1"):    #if '0' is sent from the Android App, turn OFF the LED
			client_socket.send("Recording Video!\n")
			t = threading.Thread(target=vidworker)
			threads.append(t)
			t.start()
		if (data == "q"):
			print("Quit")
			camera.close()
			client_socket.send("Quit command accepted: Shutting Down All Recording!")
			break

except KeyboardInterrupt:  
		# here you put any code you want to run before the program   
		# exits when you press CTRL+C  
	camera.close()
	client_socket.close()
	server_socket.close()
	print("\n", counter) # print value of counter

finally:  
	GPIO.cleanup() # this ensures a clean exit     