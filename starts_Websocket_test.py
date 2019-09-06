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
"""
Voici le code Python pour tester le serveur WebSocket. Veuillez noter que la m茅thode recv() 
renvoie le premier message en file d'attente, qui n'est pas n茅cessairement le plus r茅cent.
"""
from websocket import create_connection
ws = create_connection('ws://mPy.local')
result =  ws.recv()
print(result)
ws.send('Hello World')
ws.close()
"""
Avant de cr茅er une application React sur le Raspberry Pi, il est actuellement n茅cessaire de 
mettre 脿 niveau la version de Node.js fournie avec Raspbian. Commencez par supprimer les 
programmes de n艙ud existants : 
sudo apt-get remove nodered -y
sudo apt-get remove nodejs and nodejs-legacy -y

Next curl est utilis茅 pour t茅l茅charger et ex茅cuter n-install, qui installe le gestionnaire de 
versions de Node.js et met 脿 jour Node.js et NPM vers les derni猫res versions : 
curl -L https://git.io/n-install | bash

Un red茅marrage est requis apr猫s la mise 脿 niveau du n艙ud. Ensuite, utilisez curl pour installer
un gestionnaire de d茅pendances appel茅 Yarn, qui facilite la cr茅ation d'applications React. 
Un autre red茅marrage sera n茅cessaire apr猫s l'installation de Yarn :
curl -o- -L https://yarnpkg.com/install.sh | bash

Le moyen le plus simple de se familiariser avec React consiste 脿 utiliser le yarn create 
react-app (fil cr茅atif react-app) :
yarn create react-app YOUR-APP-NAME

Le kit de d茅marrage create react-app g茅n猫re une application React.js et ne n茅cessite aucune 
configuration de construction. Il n'est pas n茅cessaire de jouer avec WebPack ou Babel. 
Tout est pr茅configur茅 pour vous et vous pouvez commencer 脿 茅crire du code. Il existe 茅galement 
un serveur de d茅veloppement qui s'actualise automatiquement lorsque le code est modifi茅.
Pour t茅l茅charger le d茅p么t React pour ce tutoriel, utilisez git clone. Changez ensuite dans
le dossier t茅l茅charg茅 et utilisez Yarn pour installer et d茅marrer : 
git clone https://github.com/rdagger/React-WebSocket-Client-DS18b20.git
cd React-WebSocket-Client-DS18b20
yarn install
yarn start

Voici l'application React affichant les donn茅es du capteur de temp茅rature. 
voir starts_Websocket.jpg
La version LoBo prend 茅galement en charge le capteur de temp茅rature / humidit茅 DHT22 . 
Voici un exemple de code pour interroger le capteur DHT22:
"""
from machine import DHT, Pin
pin = 23
dht = DHT(Pin(pin), DHT.DHT2X)
result, temperature, humidity = dht.read()
if not result:
    print('Error!')
else:
    print('{0}掳C {1}%'.format(temperature, humidity))

