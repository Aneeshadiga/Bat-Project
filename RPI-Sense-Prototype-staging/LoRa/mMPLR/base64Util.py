import base64
import os 
from mMPLR.ImageUtil import ImageAdapter

class B64Util():
    
    def __init__(self):
        self.B64String = b''
        self.Filetype = 0 #0 - Text, 1 - Sensor, 2 - Image, 3 - Audio, 4 - Control
        
    def getStringFromFile(self, inputFile="./Data/input.txt", compress=True):
        if not self.setInputFile(filepath=inputFile): raise Exception("Invalid Filepath")
        if self.isDataImageorAudio() and compress: ImageAdapter().compressImage(inputFile)
        with open(self.Filepath, "rb") as f:
            __bytes = f.read()
            self.B64String = base64.b64encode(__bytes) if self.isDataImageorAudio() else __bytes
        return self.B64String.decode()
    
  
    def setInputFile(self, filepath):
        self.Filepath = os.path.abspath(filepath)
        if (filepath.endswith(".flac") or filepath.endswith(".wav")): self.Filetype = 3
        elif (filepath.endswith(".jpg") or filepath.endswith(".jpeg") or filepath.endswith(".png")): self.Filetype = 2
        elif (filepath.endswith(".txt")): self.Filetype = 0
        else: 
            #print("Invalid Input File Path") 
            return 0
        return 1

    def setOutputPath(self, filepath):
        self.OutputPath = filepath

    def getOutputPath(self):
        return self.OutputPath

    def getB64DecodedString(self, input):
        _64_decode = base64.b64decode(input)
        return _64_decode
    
    def isDataImageorAudio(self):
        return True if self.getDataType() in {2,3} else False

    def getDataType(self):
        return self.Filetype

    def writeStringToFile(self, input=b'', outFile="./Data/output", 
                        dataType=0):
        extension = {0:"Text.txt", 1:"Sens.txt", 2:"Image.jpg", 3:"Audio.flac"}
        outFile = os.path.abspath(outFile)+extension.get(dataType,".txt")
        self.setOutputPath(outFile)
        decodedString = self.getB64DecodedString(input=input) if dataType in {2,3} else input
        with open(outFile, 'wb') as _result: # create a writable image and write the decoded result
            _result.write(decodedString)

if __name__ == "__main__":
    B64 = B64Util()
    #print(B64.setInputFile("filename"))
    print(B64.getB64String())
    print(B64.getB64String().decode('utf-8'))
    B64.writeToFile()

    B64.setInputFile("./Data/captured_img.jpg")
    B64.getB64String()
    B64.setOutputPath("./Data/output.jpg")
    B64.writeToFile()
