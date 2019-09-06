"""
- Appeler deepsleep() sans argument mettra l'appareil en veille ind茅finiment
- Une r茅initialisation du logiciel ne change pas la cause de la r茅initialisation
- Il peut y avoir un courant de fuite traversant les tractions internes activ茅es. 
  Pour r茅duire davantage la consommation d'茅nergie, il est possible de d茅sactiver les trames
  internes:
  p1 = Pin(4, Pin.IN, Pin.PULL_HOLD)

 Apr猫s avoir dormi profond茅ment, il peut 锚tre n茅cessaire de d茅verrouiller explicitement la 
 broche (par exemple, s'il s'agit d'une broche de sortie) via:
 p1 = Pin(4, Pin.OUT, None)

 The following code can be used to sleep, wake and check the reset cause:
"""

import machine

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')

# put the device to sleep for 10 seconds
machine.deepsleep(10000)
