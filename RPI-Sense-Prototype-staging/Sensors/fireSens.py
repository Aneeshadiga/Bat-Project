#Python code to send the real time data of temperature and light sensors to Firebase
#Import Temp & light sensors supporting codes

from .BME.BME import *
from .GPS.gps import *
from .Light.bh1750 import *

import sys
sys.path.append('../RPI-SENSE-PROTOTYPE')
from util import *
from fireInit import getFirebaseInstance
from collections import OrderedDict

class FireSensor:
    def __init__(self) -> None:
        self.db = getFirebaseInstance().database()

    def getSensData(self):
        BMEdata = BME().getBMEData()
        lightVal = LightSensor().readLight()
        return OrderedDict({"Temperature":round(BMEdata[0],2), "Humidity":round(BMEdata[3],2), "Pressure":round(BMEdata[2],2), "LightIntensity":round(lightVal,2)})

    def pushSensData(self):
        self.db.child(getDate()).child(getTime()).set(self.getSensData())
        print("Sensor Values Uploaded Successfully.")

    def getGPSCoordinates(self):
        return GPS().getCoordinates()

    def postGPSCoordinates(self):
        self.db.child("Location").set(self.getGPSCoordinates())

    def sense(self):
        BME().displayBME()
        LightSensor().putLightValues()
        self.pushSensData()
    
if __name__=="__main__":
   FireSensor().sense()
