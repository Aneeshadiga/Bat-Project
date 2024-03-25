#import tinify
import os 
#from dotenv import load_dotenv
from PIL import Image

class ImageAdapter:
    def __init__(self) -> None:
        #load_dotenv()
        #tinify.key = os.environ.get('TinyAPIKey')
        #print(tinify.key)
        pass
        

    def compressImage(self, imagepath="./Data/input.png"):
        #source = tinify.from_file(os.path.abspath(imagepath))
        #source.to_file(imagepath)
        picture = Image.open(os.path.abspath(imagepath))
        w,h = picture.size
        picture = picture.resize((w//4,h//4))
        picture.save(os.path.abspath(imagepath), 
                 "JPEG", 
                 optimize = True, 
                 quality =10)

if __name__ == "__main__":
    imageAdapter = ImageAdapter()
    imageAdapter.compressImage()