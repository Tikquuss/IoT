import esp

esp.osdebug(None)       # turn off vendor O/S debugging messages
						# d鑼卻active les messages de d鑼卋ogage du fournisseur

esp.osdebug(0)  # redirect vendor O/S debugging messages to UART(0)
				# redirige les messages de d鑼卋ogage du syst鐚玬e d'exploitation 
				# du fournisseur vers UART (0)

# m鑼卼hodes de bas niveau pour interagir avec le stockage flash
# low level methods to interact with flash storage
print(esp.flash_size())
print(esp.flash_user_start())
print(esp.flash_erase(sector_no))
print(esp.flash_write(byte_offset, buffer))
print(esp.flash_read(byte_offset, buffer))