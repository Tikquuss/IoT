from machine import TouchPad, Pin

t = TouchPad(Pin(14))
t.read()              # Returns a smaller number when touched

"""
TouchPad.read renvoie une valeur relative 脿 la variation capacitive. 
Les petits nombres (typiquement dans les dizaines ) sont courants quand une 茅pingle est 
touch茅e, les plus grands nombres (plus de mille ) quand aucun contact n'est pr茅sent. 
Cependant, les valeurs sont relatives et peuvent varier en fonction du tableau et de la 
composition environnante. Un 茅talonnage peut donc 锚tre n茅cessaire.
Il existe dix broches capacitives tactiles qui peuvent 锚tre utilis茅es sur l'ESP32:
0, 2, 4, 12, 13, 14, 15, 27, 32, 33. 
Essayer d鈥檃ffecter des broches 脿 d鈥檃utres entra卯nera une erreur ValueError .

Notez que les TouchPads peuvent 锚tre utilis茅s pour sortir un ESP32 du mode veille:
"""
import machine
#from machine import TouchPad, Pin
import esp32

t = TouchPad(Pin(14))
t.config(500)               # configure the threshold at which the pin is considered touched
esp32.wake_on_touch(True)
machine.lightsleep()        # put the MCU to sleep until a touchpad is touched