"""
Il se connecte au Wi-Fi puis lance les services mDNS, FTP et Telnet.
Une fois ce code ex茅cut茅 dans le main.py de l'esp32, red茅marr茅. L'ESP32 peut 锚tre maintenant 
g茅r茅 sans fil via Telnet et FTP. 
Avec l'ex茅cution de mDNS, l'ESP32 peut maintenant 锚tre r茅f茅renc茅 par le nom mDNS fourni au 
lieu d'une adresse IP. Pour l'exemple ci-dessus, vous pouvez envoyer une requ锚te ping 脿 l'ESP32
depuis un autre ordinateur 脿 l'aide de mPy.local: ping mPy.local -c 1

Probleme pour moi : mDNS est int茅gr茅 脿 Linux et Mac. Il ne vient pas avec Windows.
Solution : Il peut facilement 锚tre ajout茅 en installant un programme gratuit appel茅 
Bonjour (https://support.apple.com/downloads/bonjour_for_windows). 
Si vous avez iTunes, il est probablement d茅j脿 install茅 sur votre ordinateur.
"""
from network import mDNS, ftp, telnet, STA_IF, WLAN
from machine import idle
mdns = mDNS()
wlan = WLAN(STA_IF)
wlan.active(True)
nets = wlan.scan()
for net in nets:
    ssid = net[0]
    if ssid == b'YOUR_SSID':
        wlan.connect(ssid, 'YOUR_PASSWORD')
        while not wlan.isconnected():
            idle() # save power while waiting
        print('WLAN connection succeeded!')
        mdns.start('mPy', 'MicroPython ESP32')
        ftp.start(user='YOUR_USERNAME', password='YOUR_PASSWORD')
        telnet.start(user='YOUR_USERNAME', password='YOUR_PASSWORD')
        break