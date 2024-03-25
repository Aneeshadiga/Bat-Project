import usb.core
import usb.util

class SerialAdapter:
    def __init__(self, productID = 0xea60, vendorID = 0x10c4) -> None:
        self.dev = usb.core.find(idVendor=vendorID, idProduct=productID)
        if self.dev is None:
            raise ValueError('Device not found')
        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        i = 0 #if self.dev[0].interfaces()[0].bInterfacenumber else 0

        
        if self.dev.is_kernel_driver_active(i):
            try:
                self.dev.detach_kernel_driver(i)
            except usb.core.USBError as e:
                sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))
        #self.dev.set_configuration()

    def send(self, data):
        # write the data
        self.device.write(data)
        assert len(self.dev.write(1, data, 100)) == len(data)

    def read(self, leng):
        try: 
            ret = self.dev.read(0x81, leng, 100)
            sret = ''.join([chr(x) for x in ret])
            return sret
        except: return ""

    