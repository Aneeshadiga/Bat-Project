"""
SoundDevice: Record Audio as Numpy Array
Scipy.io.wavfile: writing the wave file
Pydub: Converting to FLAC and adding the Tags to it
"""
import sys
sys.path.insert(0,"../")
from fireInit import getFirebaseInstance
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import datetime;
import os

class AudioRecorder:

    def __init__(self) -> None:
        self.SITE = getFirebaseInstance().database().child("SITE").get().val() or "TestSite"
        self.WAVE_OUTPUT_FILENAME = os.environ.get('WAVE_OUTPUT_FILENAME', "audioRecord.wav")
        self.FLAC_OUTPUT_FILENAME = os.environ.get('FLAC_OUTPUT_FILENAME', "audioRecordFLAC_test.flac")
        

    #record using sounddevice and store as numpy array    
    def recordAudio(self, duration = 5, rate = 44100):
        myrecording = sd.rec(int(duration * rate), samplerate=rate, channels=2)
        sd.wait()
        self.writeWave(myrecording, rate)

    #writing a wav file from the numpy array
    def writeWave(self, numpyRecord, rate):    
        write(self.WAVE_OUTPUT_FILENAME, rate, numpyRecord) 

    #add metadata to the wave
    def addTags(self, meta=None):
        #reading audiosegments from the written wave file
        sound = AudioSegment.from_file(self.WAVE_OUTPUT_FILENAME)
        
        if not meta:
            meta={
                "Title":"BCIT Audio Captuere: Site - " + self.SITE,
                "Organization":"bcit", 
                "TimeOfRecord":str(datetime.datetime.now())
                }

        #Adding the tags to the wave file
        sound.export(
            self.FLAC_OUTPUT_FILENAME, 
            format="flac",
            tags=meta
        )

if __name__=="__main__":
    mAudioRecorder = AudioRecorder()
    mAudioRecorder.recordAudio()
    mAudioRecorder.addTags()
