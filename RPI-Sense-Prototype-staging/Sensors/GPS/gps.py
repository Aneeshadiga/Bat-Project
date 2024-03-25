import serial
import pynmea2
import pprint

class GPS:
    def __init__(self) -> None:
        self.gpsPort = "/dev/ttyAMA0"  #"/dev/ttyTHS1"
        self.gpsSerial= serial.Serial(
            self.gpsPort, 
            baudrate=9600, 
            timeout=0.5)

    def getCoordinates(self):
        newdata = self.gpsSerial.readline()
        if newdata[0:6] == b"$GPRMC":
            newmsg=pynmea2.parse(newdata.decode("utf-8"))
            lat=newmsg.latitude
            lng=newmsg.longitude
            gps = {"Latitude": str(lat), "Longitude":str(lng)}
            pprint(gps)
            return gps
        return ""

if __name__=="__main__":
    GPS().getCoordinates()
