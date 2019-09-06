#Auteur : Pascal Tikeng
# Note : 
"""
Cette classe permet de faire clignoter un LED chaque 'sleep' ms
"""

try:
    import gc
except ImportError:
    raise ImportError("module gc not found")

try:
    from machine import Pin
    gc.collect()
except ImportError:
    raise ImportError("python-machine.Pin not found")
    
try:
    from time import sleep
    gc.collect()
except ImportError:
    raise ImportError("time.sleep not found")
    
class Led(object):
    _pin = 2
    _sleep = 0 #pas de clignoter en continue

    def __init__(self, pin=2, sleep=0):
        self._pin=pin
        self._sleep=sleep
        
    def bling(self) :
        if(self._sleep == 0) :
            machine.Pin(self._pin, machine.Pin.OUT).value(1)
        else :
            led = Pin(self._pin, Pin.OUT)
            while True :
                led.value(not led.value())
                sleep(self._sleep)
    
    def stop(self, after = 0) :
        # arreter le LED
        sleep(after)
        machine.Pin(self._pin, machine.Pin.OUT).value(0)
            
  
def main() :
  	led = Led(pin = 2, sleep = 1)
    led.bling()
    #led.stop()

if __name__ == '__main__' :
  	main()








