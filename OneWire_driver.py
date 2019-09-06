from machine import Pin
import onewire

# Le pilote OneWire est impl茅ment茅 dans le logiciel et fonctionne sur toutes les broches:
import onewire
ow = onewire.OneWire(Pin(12)) # create a OneWire bus on GPIO12
ow.scan()               # return a list of devices(p茅riph茅riques) on the bus
ow.reset()              # reset the bus
ow.readbyte()           # read a byte
ow.writebyte(0x12)      # write a byte on the bus
ow.write('123')         # write bytes on the bus
ow.select_rom(b'12345678') # select a specific device by its ROM code
						   # s茅lectionne un p茅riph茅rique en fonction de son code ROM

"""
Il existe un pilote sp茅cifique pour les p茅riph茅riques DS18S20 et DS18B20.
Assurez-vous de mettre une r茅sistance de traction de 4,7k sur la ligne de donn茅es. 
Notez que la m茅thode convert_temp() doit 锚tre appel茅e 脿 chaque fois que vous souhaitez 
茅chantillonner la temp茅rature.
"""
ow = onewire.OneWire(Pin(12)) 
ow.scan() 

def main() :
	import time, ds18x20
	ds = ds18x20.DS18X20(ow)
	roms = ds.scan()
	ds.convert_temp()
	time.sleep_ms(750)
	for rom in roms:
	    print(ds.read_temp(rom))

if __name__ == "__main__":
	#Assurez-vous de mettre une r茅sistance de traction de 4,7k sur la ligne de donn茅es
    #main()

