#loads env variables
from dotenv import load_dotenv
load_dotenv()

import pyrebase
import os

FIREBASE_CONFIG = {
    "apiKey": os.environ['APIKEY'],
    "authDomain": os.environ['authDomain'],
    "databaseURL": os.environ['databaseURL'],
    "projectId": os.environ['projectId'],
    "storageBucket": os.environ['storageBucket'],
    "messagingSenderId": os.environ['messagingSenderId'],
    "appId": os.environ['appId'],
    "measurementId": os.environ['measurementId']
}

def getFirebaseInstance():    
    config = FIREBASE_CONFIG
    firebase = pyrebase.initialize_app(config)
    return firebase