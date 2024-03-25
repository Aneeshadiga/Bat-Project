from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import os

class RPiCam:

    def __init__(self, PIN = 23, PrevMode = True, Intv = 2):
        self.camera = PiCamera()
        self.PIN_NO = PIN
        self.PREVIEW = PrevMode
        self.SLEEP = Intv
        
        self.CAPTURE_PATH = os.environ.get('CAPTURE_PATH') or "/home/pi/Pictures/capture.jpg"
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(PIN, GPIO.OUT, initial=GPIO.HIGH) # Set pin 11 to be an output pin and set initial value to high (off)
        print("Camera Initialized.\nFlash Installed at GPIO"+str(self.PIN_NO))

    def capture(self):
        if(self.PREVIEW):
            self.camera.start_preview()
            GPIO.output(self.PIN_NO, GPIO.LOW)
            sleep(self.SLEEP)
            self.camera.capture(self.CAPTURE_PATH)
            self.camera.stop_preview()
            GPIO.output(self.PIN_NO, GPIO.HIGH)
        else:
            GPIO.output(self.PIN_NO, GPIO.LOW)
            sleep(self.SLEEP)
            self.camera.capture(self.CAPTURE_PATH)
            GPIO.output(self.PIN_NO, GPIO.HIGH)
        print("Capture Successful.")

    def closeCam(self):
        GPIO.cleanup()
        print("Camera Shut-Down.")
    
if __name__=="__main__":
   rpicam = RPiCam()
   rpicam.capture()
   rpicam.closeCam()
