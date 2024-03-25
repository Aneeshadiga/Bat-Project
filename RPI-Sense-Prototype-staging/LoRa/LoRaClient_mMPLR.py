#!/usr/bin/env python3

""" This program sends a response whenever it receives the "CNT" """

# Copyright 2022 zOrOjUrO.
#
# This file is part of pySX127x-mMPLR, a fork of rpsreal/pySX127xw which is fork of mayeranalytics/pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.
import string
import random
import logging
import time
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

from mMPLR.mMPLR import mMPLR
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from Sensors.fireSens import FireSensor
from Camera.fireCam import FireCam
from Audio.fireAudio import FireAudio
os.chdir(parentdir)
BOARD.setup()
BOARD.reset()
#parser = LoRaArgumentParser("Lora tester")


class mMPLRLoraClient(LoRa):
    def __init__(self, verbose=False):
        super(mMPLRLoraClient, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.bretry_attempts = 0
        self.state = 0
        self.mplr = mMPLR(devId=1,batchSize=10)
        self.currentBatch = 0
        self.resendingBatch = []
        self.corrupt = []
        self.nBatches = 0
        self.getSensorData = FireSensor()
        
    def clearInit(self):
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.bretry_attempts = 0
        self.state = 0
        self.mplr = mMPLR(devId=1,batchSize=10)
        self.currentBatch = 0
        self.resendingBatch = []
        self.corrupt = []
        self.nBatches = 0
        self.getSensorData = FireSensor()
        
    
    def sendData(self, raw):
        data = [int(hex(c), 0) for c in raw]
        #print("\nSending : ")#,bytes(data))
        self.write_payload(data)
        BOARD.led_on()
        self.set_mode(MODE.TX)
        time.sleep(1)

    def on_rx_done(self):
        BOARD.led_on()
        self.clear_irq_flags(RxDone=1)
        p = self.read_payload(nocheck=True)
        pkt = bytes(p)
        BOARD.led_off()
        try:
            packet = self.mplr.parsePacket(rawpacket=pkt)
            header = packet.get("Header")
            flag = header.get("Flag")
            dataType = header.get("Service")
            #print()
            #check for SYN packet
            if flag == 0:
                print("\nSYN Received")
                self.destId = header.get("DeviceUID")
                
                #check which type of data is requested 
                if dataType == 0: #0 for text
                    print("Request for text data received")
                    self.batches = self.mplr.getBatchesFromFile(destinationId=self.destId, 
                                                                filepath="Data/input.txt", 
                                                                isEncrypted=True)
                    
                elif dataType == 1: #1 for sensorData
                    #getsensor data and send
                    print("Request for sensor data received")
                    sensorData = str(self.getSensorData.getSensData())
                    self.batches = self.mplr.getPacketsAsBatches(data = sensorData,
                                                                dataType="1", 
                                                                destinationId=self.destId,
                                                                isEncrypted=True)
                    

                elif dataType == 2: #2 for image 
                    #implement capture image and store in input.png
                    print("Request for image data received")
                    #FireCam(pin=23, prevMode=True, interval=2).captureOnce()
                    self.batches = self.mplr.getBatchesFromFile(destinationId=self.destId, 
                                                                filepath="Data/image.jpg", 
                                                                isEncrypted=True,
                                                                compress=False)
                    
                elif dataType == 3: #3 for audio
                    #implement capture audio and store in input.wav
                    print("Request for audio data received")
                    #FireAudio().recordOnce(duration = 5, rate = 44100)
                    self.batches = self.mplr.getBatchesFromFile(destinationId=self.destId, 
                                                                filepath="Data/crickets.flac", 
                                                                isEncrypted=True)          
            
                
                time.sleep(2) # Wait for the client be ready            
                self.state = 1
                self.bretry_attempts = 0
                
            #check for ACK packet
            elif flag==5:                
                
                if self.state == 1:
                    print("\nReceived ACK")
                    print("\nSending ", str(self.mplr.Batches), " Batches of Packets.\n\n" )
                    time.sleep(2)
                    self.state = 2
                    #sending data
                    

                #check for ACK packet in FIN received state    
                elif self.state == 5:
                    print("\nFIN-ACK received")
                    print("Sending: ACK")
                    ack = self.mplr.genFlagPacket(DestinationID=self.destId, Service=0, BatchSize=self.mplr.BatchSize, Flag=5)
                    #self.sendData(ack)
                    self.set_mode(MODE.SLEEP)
                    print("\nConnnection Terminated")
                    self.state = 0
                    #time.sleep(2)
                    self.reset_ptr_rx()
                    self.set_mode(MODE.RXCONT)
                    print("\n\nListening for new Connections . . .\n\n")
                    self.clearInit()

            #check for Batch-ACK packet
            elif flag==3 and self.state == 3:
                print("Batch ACK received")
                #print(packet)
                payloadSize = header.get("PayloadSize")
                payload = packet.get("Content")
                time.sleep(2)
                if payloadSize == 0:
                    #implement moving to next here or in state 2
                    self.currentBatch += 1
                    if self.currentBatch > len(self.batches)-1:
                        
                        self.state = 4  #all batches sent goto FIN sending state
                        #print("state changed to ",self.state)
                    else:
                        self.state = 2  #send next batch state
                        #print("state changed to ",self.state)

                else:
                    self.resendingBatch = list(map(int, bytes(payload).decode("utf-8").split(",")))
                    self.state = 6  #resending requested batch
                    p#rint("state changed to ",self.state)

                
            #check for FIN packet    
            elif flag == 4:
                time.sleep(2)
                self.state = 4
            
                
            else:
                time.sleep(5)
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT)
        except Exception as e:
            logging.error(e, exc_info=True)
            print("\nCorrupt or Ill-formed Packet Received\n")

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        print("\nClient Initialized\n")
                
        while True:
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            while self.state == 0:
                pass;
            

            #state after receiving syn
            while self.state == 1: 
                initBatchSize = self.mplr.getBatchSize() if self.mplr.Batches == 1 else self.mplr.maxBatchSize
                synack = self.mplr.genFlagPacket(DestinationID=self.destId,
                                            Service=0,
                                            BatchSize=initBatchSize,
                                            Flag=1,
                                            Payload="#Batches:"+str(self.mplr.Batches))
                print ("Sending: SYN-ACK")
                self.sendData(synack)
                self.set_mode(MODE.SLEEP)
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT)
                #time.sleep(2)
                start_time = time.time()
                while (time.time()-start_time < 10) and self.state == 1:
                    pass;
                self.bretry_attempts += 1
                if self.bretry_attempts == 5:
                    print("\n\nNo Response.\nDisconnected\n")
                    self.state = 0
                    self.bretry_attempts = 0
                    print("\n\nListening for new Connections . . .\n\n")
                    self.clearInit()
                
            #packets/batches sending state    
            while self.state == 2: 
                #time.sleep(3)
                count = 0
                for seq, packet in enumerate(self.batches[self.currentBatch]):
                    
                    
                    count += 1
                    if count == 3 and self.currentBatch == 0:
                        print(packet)
                        print("skipped 3rd")
                        continue
                    
                    print("\nSend: DATA ", str(self.currentBatch), ".",str(seq))
                    ##print(packet)
                    self.sendData(packet)
                    self.set_mode(MODE.TX)
                    time.sleep(1)             
                self.set_mode(MODE.SLEEP)
                self.state = 3
                self.bretry_attempts = 0
            
            #waiting for batchAck    
            while self.state == 3: 
                print("Waiting for BatchAck")
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) #wait for batch ack
                #time.sleep(1)                
                start_time = time.time()
                while self.state ==3 and (time.time() - start_time < (len(self.batches[0]) * 7)):
                    # wait until receive batch ack or 10s
                    #print(self.state)
                    if self.state != 3:
                        break
                    pass;
                self.bretry_attempts += 1
                if self.bretry_attempts == 5:
                    print("\n\nNo Response.\nDisconnected\n")
                    self.state = 0
                    self.bretry_attempts = 0
                    print("\n\nListening for new Connections . . .\n\n")
                    self.clearInit()
                
           
            #FIN sending state should be done when all batches are sent
            while (self.state == 4) or self.state == 5: 
                self.currentBatch = 0
                self.batches.clear()
                fin = self.mplr.genFlagPacket(DestinationID=self.destId,
                                                Service=0,
                                                BatchSize=self.mplr.BatchSize,
                                                Flag=4)
                print("Sending: FIN")
                self.sendData(fin)
                self.state = 5
                self.set_mode(MODE.SLEEP)
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT)
                #time.sleep(2)
                start_time = time.time()
                while (time.time() - start_time < 10) and self.state == 5: # wait until receive back or 10s
                    pass;
            

            #resending requested packets from prev batch
            while self.state == 6:
                print("\nResending missed/corrupt packets: ",str(self.resendingBatch))
                for idx in self.resendingBatch:
                    self.sendData(self.batches[self.currentBatch][idx])
                    self.set_mode(MODE.TX)
                    time.sleep(1)             
                self.set_mode(MODE.SLEEP)
                self.state = 3 #BatchAck state
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) #wait for batch ack
                #time.sleep(1)
                
                start_time = time.time()
                while (time.time() - start_time < 10): # wait until receive batch ack or 10s
                    pass;
                    
                
                
                
            

lora = mMPLRLoraClient(verbose=False)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py

#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_bw(BW.BW125)
#lora.set_coding_rate(CODING_RATE.CR4_8) 
#lora.set_spreading_factor(12)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(7)
lora.set_rx_crc(True)
#lora.set_lna_gain(GAIN.G1)
#lora.set_implicit_header_mode(False)
lora.set_low_data_rate_optim(True)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)



assert(lora.get_agc_auto_on() == 1)

try:
    print("START")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
BOARD.teardown()


