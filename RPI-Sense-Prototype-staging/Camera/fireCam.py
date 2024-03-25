import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import util
from fireInit import getFirebaseInstance
from Camera.rpiCam import *
from num2words import num2words

class FireCam:

    def __init__(self, pin, prevMode, interval):
        self.PHOTO_PATH = os.environ.get('CAPTURE_PATH', "/home/pi/Documents/RPI-Sense-Prototype/Data/captured_img.jpg")   
        self.Camera = RPiCam(PIN = pin, PrevMode = prevMode, Intv = interval)

    def pushImage(self):
        instance = getFirebaseInstance()
        storage = instance.storage()
        db = instance.database()
        date = util.getDate()
        captureNo = 1
        try:
            captureNo = db.child(date).child("Control").child("ClicksToday").get().val() or 1
        except: pass
        storage.child(date).child("Images").child(str(num2words(captureNo))+'.jpg').put(self.PHOTO_PATH)
        db.child(date).child("Control").child("ClicksToday").set(int(captureNo)+ 1)
        print("Image Uploaded Successfully.")

    def newCapture(self):
        self.Camera.capture()
        #self.pushImage()

    def captureOnce(self):
        self.newCapture()
        self.Camera.closeCam()
    
if __name__=="__main__":
   FireCam(pin=23, prevMode=True, interval=2).captureOnce()
