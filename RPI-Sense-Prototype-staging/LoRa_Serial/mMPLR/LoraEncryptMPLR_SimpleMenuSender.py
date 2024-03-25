#!/usr/bin/env python

""" A beacon transmitter class to send 255-byte message in regular time intervals. """
"""
# Copyright 2015 Mayer Analytics Ltd.
"""

import os
import sys 
from time import sleep
#from LoRa.pySX127x.SX127x.LoRa import LoRa
sys.path.insert(0, '../../pySX127x')
sys.path.insert(0, '../../')        
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from SecurePass import *
from mMPLR import mMPLR
import base64
import os
import base64Util
from fireProt import FirePrototype


class LoRaBeacon(LoRa):


    def __init__(self, verbose=False):
        super(LoRaBeacon, self).__init__(verbose)
        #LoRa().set_freq(434)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])
        self.tx_counter = 0
        self.Password = '2bckr0w3'
        self.mplr = mMPLR(os.environ.get('DEVICEID', 1))
        self.mplr.setDestinationID('2')
        self.mplr.setFlag('0')
        self.B64 = base64Util.B64Util()


    def on_rx_done(self):
        print("\nRxDone")
        print(self.get_irq_flags())
        packet = bytes(self.read_payload(nocheck=True)).decode('utf-8')
        print(packet)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

        initialPacket = self.mplr.parsePacket(rawpacket=packet)
        print(initialPacket)
        header = initialPacket.get("Header")
        datatype = header.get("Service")
        packets = []

        sleep(1)
        
        for _ in range(header.get("BatchSize")):
            packet = bytes(self.read_payload(nocheck=True)).decode('utf-8')
            packets.append(self.mplr.parsePacket(packet))
            self.set_mode(MODE.SLEEP)
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT)
            sleep(1)

        message = self.mplr.parsePackets(packets=packets)
        self.B64.Filetype = datatype
        types = {0:"Sensor", 1:"Image", 2:"Audio"}
        print(types.get(datatype), message)
    
    def sendData(self, raw):
        data = [int(hex(c), 0) for c in raw]
        self.write_payload(data)
        BOARD.led_on()
        self.set_mode(MODE.TX)
        sleep(1)
        
    def encryptAndSendData(self, rawData, datatype):
        encryptedData = encrypt(rawData, self.Password)
        packets = self.mplr.getPackets(data=encryptedData, dataType=datatype, destinationId = self.mplr.DestinationID)
        print("Sending ", self.mplr.BatchSize, " Packets")
        for packet in packets: 
            print("Sending Packet --> ", packet)
            self.sendData(packet)


    def on_tx_done(self):
        global args
        self.set_mode(MODE.STDBY)
        self.clear_irq_flags(TxDone=1)
        sys.stdout.flush()
        self.tx_counter += 1
        sys.stdout.write("\rtx #%d" % self.tx_counter)
        if args.single:
            print
            sys.exit(0)
        BOARD.led_off()
        sleep(args.wait)
        #inputType = input(">>> Sensor / Image / Audio: ")
        #typeOfData = {"sensor":0, "image": 1, "audio": 2}
        #dataType = typeOfData.get(inputType.lower())
        if input("\n\n1\t\t- Send Sensor Data\n\n2\t\t- Send From File\n\n") == "1":
            sensorData = FirePrototype().Sensors.getSensData()
            data = "\n"
            for key, value in sensorData.items():
                data += key+"="+str(value)+"\n"
            inp = base64.b64encode(bytes(data, 'utf-8'))
            self.B64.setB64String(inp)
            print("Sending Sensor Values..\n", data, "\n")
            self.encryptAndSendData(rawData = inp.decode('utf-8'), datatype = self.B64.Filetype)
        else:    
            filepath = input("\nFilepath: ")
            #get image or audio as base64 string
            if self.B64.setInputFile(filepath=filepath): return
            inp = (self.B64.getB64String()).decode('utf-8')
            print("Sending File...\n", inp)
            self.encryptAndSendData(rawData = inp, datatype = self.B64.Filetype)
        #self.chopNsendEncryptedData(rawinput)

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
        global args
        sys.stdout.write("\rstart")
        self.tx_counter = 0
        BOARD.led_on()
        self.set_mode(MODE.TX)
        while True:
            sleep(1)

def getArgParser():
    parser = LoRaArgumentParser("A simple LoRa beacon")
    parser.add_argument('--single', '-S', dest='single', default=False, action="store_true", help="Single transmission")
    parser.add_argument('--wait', '-w', dest='wait', default=1, action="store", type=float, help="Waiting time between transmissions (default is 0s)")
    return parser

if __name__=="__main__":
    BOARD.setup()


    lora = LoRaBeacon(verbose=False)
    args = getArgParser().parse_args(lora)

    lora.set_pa_config(pa_select=1)
    lora.set_spreading_factor(7)
    lora.set_rx_crc(True)
    #lora.set_agc_auto_on(True)
    #lora.set_lna_gain(GAIN.NOT_USED)
    #lora.set_coding_rate(CODING_RATE.CR4_6)
    #lora.set_implicit_header_mode(False)
    #lora.set_pa_config(max_power=0x04, output_power=0x0F)
    #lora.set_pa_config(max_power=0x04, output_power=0b01000000)
    #lora.set_low_data_rate_optim(True)
    #lora.set_pa_ramp(PA_RAMP.RAMP_50_us)

    print(lora)
    #assert(lora.get_lna()['lna_gain'] == GAIN.NOT_USED)
    assert(lora.get_agc_auto_on() == 1)

    print("Beacon config:")
    print("  Wait %f s" % args.wait)
    print("  Single tx = %s" % args.single)
    print("")
    try: input("Press enter to start...")
    except: pass

    try:
        lora.start()
    except KeyboardInterrupt:
        sys.stdout.flush()
        print("")
        sys.stderr.write("KeyboardInterrupt\n")
    finally:
        sys.stdout.flush()
        print("")
        lora.set_mode(MODE.SLEEP)
        print(lora)
        BOARD.teardown()
