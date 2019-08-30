# tester si on a la biblio serial : pip search serial 
import serial
port = 'COM4'
port1 = '/dev/ttyUSB0'
def main():
  dir(serial)
  #ser = serial.Serial(port1) # open serial port
  #ser.close()

if __name__ == '__main__':
   main()

import time
ser = serial.Serial('COM32', 9600, timeout=0)
while 1:
 try:
  print(ser.readline())
  time.sleep(1)
 except ser.SerialTimeoutException:
  print('Data could not be read')
  time.sleep(1)