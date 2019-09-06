import network

def access_point_config(essid) : # essid='ESP-AP' par exemple
	ap = network.WLAN(network.AP_IF) # create access-point interface
	ap.config(essid) # set the ESSID of the access point
	ap.active(True)  # activate the interface

def do_connect(essid, password):
    """Une fonction utile pour la connexion 脿 votre r茅seau WiFi local"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
def main():  
  """
	wlan = network.WLAN(network.STA_IF) # create station interface
	wlan.active(True)       # activate the interface
	print(wlan.scan())             # scan for access points
	print(wlan.isconnected())      # check if the station is connected to an AP
	print(wlan.connect('Wifi_Tikeng', 'aaaaaaaa')) # connect to an AP
	print(wlan.config('mac'))      # get the interface's MAC adddress
	print(wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses
  """
  do_connect('Wifi_Tikeng', 'aaaaaaaa')
  
if __name__ == "__main__":
	main()
    
