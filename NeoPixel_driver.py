"""
Par défaut, NeoPixel est configuré pour contrôler les unités 800 kHz les plus populaires. 
Il est possible d'utiliser une synchronisation alternative pour contrôler d'autres 
périphériques (généralement 400 kHz) en transmettant une timing=0 lors de la construction 
de l'objet NeoPixel 
"""

from machine import Pin
from neopixel import NeoPixel

pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 8)   # create NeoPixel driver on GPIO0 for 8 pixels
np[0] = (255, 255, 255) # set the first pixel to white
np.write()              # write data to all pixels
r, g, b = np[0]         # get first pixel colour

#For low-level driving of a NeoPixel/Pour la conduite à basse altitude d'un NeoPixel:

import esp
esp.neopixel_write(pin, grb_buf, is800khz)
Warning
