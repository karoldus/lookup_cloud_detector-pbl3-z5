# PBL W7
# zepół 5

# wariant pełen ("jedna lub wiele lampek-klientów z jednym lub wieloma sterownikami-klientami"):
#   - jeden serwer, który nie ma dopiętej diody LED,
#   - jedno lub wiele urządzeń klienckich, które pełnią rolę lampy z diodą LED RGB; dioda powinna świecić zgodnie z nastawami, które dyktuje serwer,
#   - jedno lub wiele urządzeń klienckich, które mogą sterować parametrami dowolnej lampy na podstawie dialogu z użytkownikiem.


# ---------------------------------- libraries -----------------------------------------
import http.client
from gpiozero import PWMLED, Device                                      
from gpiozero.pins.pigpio import PiGPIOFactory
import json
import time

# ---------------------------------- configuration -----------------------------------------

conn = http.client.HTTPConnection("192.168.0.105:5000") #change

LED_GPIO_PIN = { # pins
    'green' : 20,
    'blue' : 21,
    'red' : 16
}

Device.pin_factory = PiGPIOFactory()

led = {}
for l in list(LED_GPIO_PIN.keys()):
    led[l] = PWMLED(LED_GPIO_PIN[l])
    led[l].value = 0

ID = -1

# --------------------------------- functions ------------------------------------------

def get_all():
    conn.request("GET", "/v1/led/" + str(ID))
    resp = conn.getresponse()
    data = resp.read()
    print(resp.status, resp.reason, data)

    obj = json.loads(data)["colors"]

    for l in list(obj.keys()):
        led[l].value = obj[l]/100


def connect(): # [można dodać obsługę błędów]
    global ID
    conn.request("POST", "/v1/led") # add new device
    resp = conn.getresponse()
    data = resp.read()
    obj = json.loads(data)
    ID = int(obj['id'])
    print(resp.status, resp.reason, " New ID: ", ID)
    
    for l in list(led.keys()): # add leds
        payload = {}
        payload["color"] = l
        payload["level"] = led[l].value
        headers = {"Content-type": "application/json"}
        params =  json.dumps(payload)

        conn.request("POST", "/v1/led/" + str(ID), params, headers)

        resp = conn.getresponse()
        data = resp.read()
        print(resp.status, resp.reason, data)




# ---------------------------------- initiation -----------------------------------------
connect()


# ---------------------------------- loop -----------------------------------------

while(1):
    get_all()
    time.sleep(0.1)