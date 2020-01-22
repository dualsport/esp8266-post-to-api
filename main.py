import machine
import network
import urequests
import ujson
import urandom

LED_PIN = 2  #D4
LED2_PIN = 16  #D0
BUUTON_PIN = 14  #D5
led = machine.Pin(LED_PIN, machine.Pin.OUT)
led2 = machine.Pin(LED2_PIN, machine.Pin.OUT)
button = machine.Pin(BUUTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)



def api_post(tag, value):
    url = secrets['host'] + secrets['endpoint']
    headers = {'Content-Type': 'application/json',
               'Authorization': secrets['token']}
    data = {'tag': tag,
            'value': value}
            
    resp = urequests.post(url, data=ujson.dumps(data), headers=headers)

    print('\n' + str(resp.status_code))
    print(resp.reason.decode('utf-8'))
    print(resp.json())
    
    if resp.status_code == 201:
        return 1
    else:
        return 0
        
        
def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val



print('\n\n')
with open('secrets.json') as f:
    secrets = ujson.loads(f.read())
    
# Turn off access point
ap = network.WLAN(network.AP_IF)
ap.active(False)

# Setup WiFi connection.
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wifis = wlan.scan()
    for wifi in wifis:
        print(wifi)
    print('\nConnecting to WiFi.')
    wlan.active(True)
    wlan.connect(secrets['ssid'], secrets['pass'])
    while not wlan.isconnected():
        machine.idle()
print('Connected to ' + secrets['ssid'])
print('Network config:', wlan.ifconfig())

while True:
    value = randint(1, 1000)
    if not button.value():
        led.on()
        led2.off()
        p = api_post('test_integer', value)
        led2.on()
        if p == 1:
            led.off()
            


