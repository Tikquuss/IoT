"""
Les broches disponibles sont dans les gammes suivantes (inclus): 0-19, 21-23, 25-27, 32-39. 
Celles-ci correspondent aux num茅ros de broches GPIO r茅els de la puce ESP32. 
Notez que de nombreuses cartes d'utilisateurs finaux utilisent leur propre num茅rotation 
de broches ad hoc (marqu茅e par exemple D0, D1, ...). Pour le mappage entre les broches 
logiques de la carte et les broches de la puce physique.

- Les broches 1 et 3 sont respectivement REPL UART TX et RX
- Les broches 6, 7, 8, 11, 16 et 17 sont utilis茅es pour connecter le flash int茅gr茅 et 
  ne sont pas recommand茅es pour d'autres utilisations.
- Les broches 34 脿 39 sont uniquement des entr茅es et n'ont pas non plus de r茅sistances 
  de rappel internes
- La valeur d'extraction de certaines broches peut 锚tre d茅finie sur Pin.PULL_HOLD afin 
  de r茅duire la consommation d'茅nergie pendant le sommeil profond.
"""

from machine import Pin

p0 = Pin(0, Pin.OUT)    # create output pin on GPIO0
p0.on()                 # set pin to "on" (high) level
p0.off()                # set pin to "off" (low) level
p0.value(1)             # set pin to on/high

p2 = Pin(2, Pin.IN)     # create input pin on GPIO2
print(p2.value())       # get value, 0 or 1

p4 = Pin(4, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistor, Activer la r茅sistance de tirage interne
p5 = Pin(5, Pin.OUT, value=1) # set pin high on creation