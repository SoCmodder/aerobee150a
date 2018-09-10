from bluetooth import *
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import picamera
import datetime
import time
import threading
import BMP280 as BMP280
import logging

# Initialize Pressure and Temp Sensor
#sensor = BMP280.BMP280()

# Initialize Camera
camera = picamera.PiCamera()
camera.resolution = (1280, 720)

# Initialize Bluetooth Socket
server_socket=BluetoothSocket( RFCOMM )

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
									 profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
										)

threads = []

#f = open("bt-activated-data-recording.txt","w") 

#initAlt = sensor.read_altitude() 

#def altworker():
#	"""thread worker function"""
#	for i in range(0, 960):
#		f.write('======================================================================\n')
#		f.write('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '\n')
#		f.write('Temp = {0:0.2f} *C'.format(sensor.read_temperature()) + '\n')
#		f.write('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()) + '\n')
#		f.write('Altitude = {0:0.2f} m'.format(sensor.read_altitude()) + '\n')
#		f.write('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()) + '\n')
#		f.write('======================================================================\n\n')
#		client_socket.send('Altitude = {0:0.2f} m'.format(sensor.read_altitude() - initAlt) + '\n')
#		time.sleep(1)
	#Save/Close the file
#	f.close()
#	client_socket.send("Finished Altitude Data Recording!\n")
#	return 

def vidworker():
	""" thread worker function for video capture """
	camera.start_recording('bt-activated-video.h264.mp4')
	camera.wait_recording(960)
	camera.stop_recording()
	camera.close()
	client_socket.send("Finished Recording Video")
	return 
 
client_socket,address = server_socket.accept()
print "Accepted connection from ",address

try:
	while 1:
		data = client_socket.recv(1024)
		print "Received: %s" % data

		if (data == "1"):    #if '0' is sent from the Android App, turn OFF the LED
			client_socket.send("Recording Video!\n")
			t = threading.Thread(target=vidworker)
			threads.append(t)
			t.start()
#		if (data == "2"):    #if '1' is sent from the Android App, turn OFF the LED
#			client_socket.send("Recording Data!\n")
#			t2 = threading.Thread(target=altworker)
#			threads.append(t2)
#			t2.start()
		if (data == "q"):
			print ("Quit")
			camera.close()
			client_socket.send("Quit command accepted: Shutting Down All Recording!")
			break

except KeyboardInterrupt:  
		# here you put any code you want to run before the program   
		# exits when you press CTRL+C  
	camera.close()
#	f.close()
	client_socket.close()
	server_socket.close()
	print "\n", counter # print value of counter

finally:  
	GPIO.cleanup() # this ensures a clean exit     