import serial
import time
if __name__ == '__main__':
    # if connected via USB cable
    ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1) #9600 is baud rate(must be same with that of NodeMCU)
    # if connected via serial Pin(RX, TX)
    #ser = serial.Serial('/dev/ttyS0', 9600, timeout=1) #9600 is baud rate(must be same with that of NodeMCU)
    ser.flush()
while True:
        #string = input("enter string:") #input from user
        #string = string +"\n" #"\n" for line seperation
        #string = string.encode('utf_8')
        #ser.write(string) //sending over UART
        line = ser.readline()[:-2]
        print("received: ",line)
        time.sleep(1) #delay of 1 second