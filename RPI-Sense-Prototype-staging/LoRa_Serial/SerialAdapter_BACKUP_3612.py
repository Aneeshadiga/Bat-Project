# import usb.core
# import usb.util
from socket import timeout
import serial

class SerialAdapter:
    def __init__(self, productID = 0xea60, vendorID = 0x10c4) -> None:
        self.dev = usb.core.find(idVendor=vendorID, idProduct=productID)
        if self.dev is None:
            raise ValueError('Device not found')
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
<<<<<<< HEAD
        #if self.dev[0].interfaces()[0].bInterfacenumber else 0
        #self.dev.set_configuration()
        #print(self.dev)
        #cfg = self.dev.get_active_configuration()
        #print(cfg)
        #intf = cfg[(0,0)]
        intf = 1
        if self.dev.is_kernel_driver_active(intf):
            try:
                self.dev.detach_kernel_driver(intf)
            except usb.core.USBError as e:
                sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(intf, str(e)))
        #self.dev.set_configuration()

    def send(self, data):
        # write the data
        self.dev.write(data)
        assert len(self.dev.write(1, data, 100)) == len(data)

    def read(self, leng, timeout = 1000):
        try: 
            ret = [self.dev.read(0x81, 1, timeout) for _ in range(leng)] 
            sret = ''.join([chr(x) for x in ret])
            return sret
        except: return ""
=======
        print(self.dev)
        # i = 0 #if self.dev[0].interfaces()[0].bInterfacenumber else 0

        
        # if self.dev.is_kernel_driver_active(i):
        #     try:
        #         self.dev.detach_kernel_driver(i)
        #     except usb.core.USBError as e:
        #         sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))
        # #self.dev.set_configuration()

        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
        except:
            try:
                self.ser = serial.Serial('dev/ttyUSB1', 9600, timeout = 1)
            except:
                self.ser = None


    def send(self, data):
        if self.dev:
            # write the data
            self.dev.write(data)
            assert len(self.dev.write(1, data, 100)) == len(data)

    def readPacket(self):
        if self.ser:
            packet = self.ser.readLine()[:-2]
            return packet
        return b''
>>>>>>> @{u}

    