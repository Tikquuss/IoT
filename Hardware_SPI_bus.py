"""
Il existe deux canaux SPI matériels qui permettent des vitesses de transmission plus rapides 
(jusqu’à 80 MHz). Celles-ci peuvent être utilisées sur toutes les broches d'E/S qui prennent
en charge la direction requise et sont par ailleurs inutilisées (voir Broches et GPIO ), 
mais si elles ne sont pas configurées sur leurs broches par défaut, elles doivent passer par une 
couche supplémentaire de multiplexage GPIO, ce qui peut avoir une incidence sur leur fiabilité à
 haute vitesse. Les canaux SPI matériels sont limités à 40 MHz lorsqu'ils 
 sont utilisés sur des broches autres que celles par défaut répertoriées ci-dessous.


		HSPI(id=1)	VSPI(id=2)
sck	    14			18
mosi	13			23
miso	12			19

Hardware SPI has the same methods as Software SPI above:
"""

from machine import Pin, SPI

hspi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
vspi = SPI(2, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))



