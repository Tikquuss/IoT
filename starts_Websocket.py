"""
Voici le code du serveur MicroPython ESP32 WebSocket (ws1.py). Il d茅marre un serveur WebSocket 
et utilise une minuterie mat茅rielle pour interroger le capteur de temp茅rature DS18b20 toutes les
3 secondes, puis transmettre les donn茅es ainsi que la temp茅rature et la dur茅e internes de 
l'ESP32 脿 tous les clients WebSocket connect茅s.

Apr猫s avoir copi茅 le contenu du fichier ci-dessous sur l'ESP32, il peut 锚tre ex茅cut茅 脿 l'aide 
de l'importation starts_Websocket et arr锚t茅 avec CTRL-C. Le serveur WebSocket peut 锚tre test茅 脿 
l'aide de la biblioth猫que Python websocket-client. Il peut 锚tre install茅 en utilisant pip :
pip3 install websocket-client

Voir le code de test dans le fichier de test : starts_Websocket_test.py.
"""
import machine
from machine import Onewire, RTC, Timer
from microWebSrv import MicroWebSrv
import json
from time import sleep

ow = Onewire(23)  # Initialize onewire & DS18B20 temperature sensor
ds = Onewire.ds18x20(ow, 0)

rtc = RTC()  # Real-time clock
rtc.ntp_sync(server='us.pool.ntp.org', tz='PST8PDT')  # Pull time from Internet

tm = Timer(0)  # Instatiate hardware timer

def cb_receive_text(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)

def cb_receive_binary(webSocket, data) :
    print("WS RECV DATA : %s" % data)

def cb_closed(webSocket) :
    tm.deinit()  # Dispose of timer
    print("WS CLOSED")

def cb_timer(timer, websocket):
    dict = {}  # Store data in dict
    dict['temp'] = ds.convert_read()  # Poll temperature sensor
    print(dict['temp'])
    dict['internal'] = machine.internal_temp()[1]  # Read ESP32 internal temp
    dict['time'] = rtc.now()  # Record current time
    websocket.SendText(json.dumps(dict))  # Convert data to JSON and send
    
def cb_accept_ws(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = cb_receive_text
    webSocket.RecvBinaryCallback = cb_receive_binary
    webSocket.ClosedCallback 	 = cb_closed
    cb = lambda timer: cb_timer(timer, webSocket)  # Use lambda to inject websocket
    tm.init(period=3000, callback=cb)  # Init and start timer to poll temperature sensor

mws = MicroWebSrv()                 # TCP port 80 and files in /flash/www
mws.MaxWebSocketRecvLen     = 256   # Default is set to 1024
mws.WebSocketThreaded       = True  # WebSockets with new threads
mws.WebSocketStackSize      = 4096
mws.AcceptWebSocketCallback = cb_accept_ws # Function to receive WebSockets
mws.Start(threaded=False)  # Blocking call (CTRL-C to exit)

print('Cleaning up and exiting.')
mws.Stop()
tm.deinit()
rtc.clear()
ds.deinit()
ow.deinit()