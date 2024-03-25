import serial
import time
import string
import pynmea2

port="/dev/ttyAMA0"	#"/dev/ttyTHS1" 
ser=serial.Serial(port, baudrate=9600, timeout=0.5)

while True:
	#dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline()
	#print(newdata)
    # print(newdata)
	if newdata[0:6] == b"$GPRMC":
		newmsg=pynmea2.parse(newdata.decode("utf-8"))
		#print(newmsg.latitude)
		lat=newmsg.latitude
		lng=newmsg.longitude
		gps = "Latitude=" + str(lat) + "\tand\tLongitude=" + str(lng)
		print(gps)

#sudo systemctl stop serial-getty@ttyAMA0.service
#sudo systemctl disable serial-getty@ttyAMA0.service


