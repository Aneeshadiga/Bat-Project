from Camera.fireCam import FireCam
from Sensors.fireSens import FireSensor
from Audio.fireAudio import FireAudio

class FirePrototype:
   def __init__(self) -> None:
      self.Camera = FireCam(pin=16, prevMode=True, interval=2)
      self.Sensors = FireSensor()
      self.Recorder = FireAudio()

if __name__=="__main__":
   prototype = FirePrototype()
   print(prototype.Sensors.getSensData())
   #print(fireSensor.getGPSCoordinates())
   prototype.Camera.captureOnce()
   FireAudio().recordOnce()
   