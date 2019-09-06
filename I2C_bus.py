"""
Le pilote I2C a des impl茅mentations logicielles et mat茅rielles, et les deux p茅riph茅riques 
mat茅riels ont des identificateurs 0 et 1. Toutes les broches compatibles avec la sortie 
disponibles peuvent 锚tre utilis茅es pour SCL et SDA. Le pilote est accessible via la classe
machine.I2C 
"""
from machine import Pin, I2C

# construct a software I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

# construct a hardware I2C bus
i2c = I2C(0)
i2c = I2C(1, scl=Pin(5), sda=Pin(4), freq=400000)

i2c.scan()              # scan for slave devices

i2c.readfrom(0x3a, 4)   # read 4 bytes from slave device with address 0x3a
i2c.writeto(0x3a, '12') # write '12' to slave device with address 0x3a

buf = bytearray(10)     # create a buffer with 10 bytes
i2c.writeto(0x3a, buf)  # write the given buffer to the slave