from fireInit import getFirebaseInstance
from util import *
from collections import OrderedDict

class FireSensorUtil:
    def __init__(self) -> None:
        self.db = getFirebaseInstance().database()
        
    def pushSensData(self, sensorData):
        self.db.child(getDate()).child(getTime()).set(sensorData)
        print("Sensor Values Uploaded Successfully.")

    def pushSensFromFile(self, filepath):
        f = open(filepath).read()
        d = eval(f)
        self.pushSensData(d)
