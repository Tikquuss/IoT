import serial
  
def scan():
    """scan for available ports. return a list of tuples (num, name)"""
    available = []
    for i in range(0,256):
        try:
            s = serial.Serial('COM'+str(i))
            available.append((i, s.portstr))
            s.close()
        except serial.SerialException:
            pass
    return available

def open_port() :
  a=serial.Serial()
  a.setPort('COM3')
  #a.setPort(2)  
  a.open()
  variable = a.read(n) # n est le nombre de bits qu'on veut lire
  a.close
  
if __name__=='__main__':
    print ("Found ports:")
    for n,s in scan():
        print ("(%d) %s" % (n,s))
    input("pause")
    #pen_port()
