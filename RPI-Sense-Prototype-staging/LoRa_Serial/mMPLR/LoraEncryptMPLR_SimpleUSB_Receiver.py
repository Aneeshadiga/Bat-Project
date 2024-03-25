#!/usr/bin/env python

""" A beacon transmitter class to send 255-byte message in regular time intervals. """
"""
# Copyright 2015 Mayer Analytics Ltd.
"""  
import inspect
import os
import sys
from time import sleep

from base64Util import B64Util
from mMPLR import mMPLR
from SecurePass import *
from fireSensCopy import *

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from SerialAdapter import SerialAdapter

serialAdapter = SerialAdapter()
mplr = mMPLR(os.environ.get('DEVICEID', 1))
Password = '2bckr0w3'
B64 = B64Util()
fireSens = FireSensor()


def getMessage(messageBytes, messageType):
    encodedBytes = bytes(getDecryptedContent(messageBytes.decode()), 'utf-8', errors='replace') 
    getDecodedContent(encodedBytes, messageType)
    return len(base64.b64decode(encodedBytes))

def getDecryptedContent(encryptedContent):
    return decrypt(encryptedContent, Password)

def getDecodedContent(encodedBytes, contentType):
    extensions = {0:".txt", 1:".jpg", 2:".flac"}
    fileExtension = extensions.get(contentType, ".txt") 
    B64.setB64String(encodedBytes)
    B64.setOutputPath("received"+fileExtension)
    B64.writeToFile()

while True:
    packet = serialAdapter.readPacket()
    if len(packet) < 16*8: continue
    try:
        initialPacket = mplr.parsePacket(rawpacket=packet)
        print(initialPacket)
    except:
        continue
    else:
        if initialPacket.get("isCorrupt", False): continue
        header = initialPacket.get("Header")
        datatype = int(header.get("Service"))
        packets = [packet]
        for _ in range(int(header.get("BatchSize"))-1):
            try:
                packet = mplr.parsePacket(rawpacket=serialAdapter.readPacket())
                print(packet)
                packets.append(packet)
            except: continue        
            sleep(1)
        messageBytes = mplr.parsePackets(packets=packets)
        B64.Filetype = datatype
        types = {0:"Sensor", 1:"Image", 2:"Audio"}
        typ = types.get(datatype)
        
        print("File Type: "+typ, "\n")
        print("Received File.\nFile length: ", getMessage(messageBytes=messageBytes, messageType = typ))
        if typ == "Sensor":
            print("Uploading data to firebase...")
        try:
            fireSens.sense()
        except:
            print("No sensor value found file didn't get uploaded to firebase")
            pass
        
        
        


