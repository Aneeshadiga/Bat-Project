import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from util import *
from fireInit import getFirebaseInstance
from Audio.audioRecMeta import AudioRecorder
from num2words import num2words

class FireAudio:

    def __init__(self) -> None:
        self.CAPTURE_PATH = os.environ.get('FLAC_OUTPUT_FILENAME', "audioRecordFLAC_test.flac")
        self.audioRecorder = AudioRecorder()

    def pushAudio(self):
        instance = getFirebaseInstance()
        storage = instance.storage()
        db = instance.database()
        date = getDate()
        captureNo = db.child(date).child("Control").child("CapturesToday").get().val() or 1
        storage.child(date).child("Audio").child(str(num2words(captureNo))+'.flac').put(self.CAPTURE_PATH)
        db.child(date).child("Control").child("CapturesToday").set(int(captureNo)+ 1)
        print("Audio Uploaded Successfully.")

    def recordOnce(self, duration = 10, rate = 44100):
        self.audioRecorder.recordAudio(duration, rate)
        self.audioRecorder.addTags()

if __name__=="__main__":
    FireAudio().recordOnce(duration = 10, rate = 44100)
