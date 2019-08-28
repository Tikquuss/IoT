# Ce petit script va simplement faire clignoter une Led branch茅e sur la broche 19 de l鈥橢SP32
import utime
import machine
pin19 = machine.Pin(19, machine.Pin.OUT)
while True:
  pin19.value(1)
  utime.sleep_ms(500)
  pin19.value(0)
  utime.sleep_ms(500)
