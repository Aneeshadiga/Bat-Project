#Python code to send the real time data of temperature and light sensors to Firebase
#Import Temp & light sensors supporting codes


import sys
#sys.path.append('../../RPI-SENSE-PROTOTYPE')
from fireutil.util import *
from fireutil.fireInit import getFirebaseInstance
from collections import OrderedDict

class FireSensor:
    def __init__(self) -> None:
        self.db = getFirebaseInstance().database()

    def getSensData(self):
        with open('received.txt') as f:
            listVal = f.readlines()
            orderedDict = OrderedDict()
            newListVal = []
            
            for i in listVal:
                splits = i.split(":")
                splits[1] = splits[1].rstrip()
                newListVal.append(splits)
                if  splits[0] == "T":
                    orderedDict["Temperature"] = splits[1]
                elif splits[0] == "H":
                    orderedDict["Humidity"] = splits[1]
                elif splits[0] == "P":
                    orderedDict["Pressure"] = splits[1]
                else:
                    orderedDict["LightIntensity"] = splits[1]
        return orderedDict

    def pushSensData(self):
        self.db.child(getDate()).child(getTime()).set(self.getSensData())
        print("Sensor Values Uploaded Successfully.")

    def getGPSCoordinates(self):
        return GPS().getCoordinates()

    def postGPSCoordinates(self):
        self.db.child("Location").set(self.getGPSCoordinates())
        

    def sense(self):        
        self.pushSensData()
        
    
    
if __name__=="__main__":
   FireSensor().sense()
    
        
