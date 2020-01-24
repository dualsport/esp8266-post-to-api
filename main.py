import machine
import network
import urequests
import ujson
import urandom
import time


LED_PIN = 2  #D4
LED2_PIN = 16  #D0
BUUTON_PIN = 14  #D5
led = machine.Pin(LED_PIN, machine.Pin.OUT)
led2 = machine.Pin(LED2_PIN, machine.Pin.OUT)
button = machine.Pin(BUUTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)


def wifi_connect(wlan, secrets):
    while not wlan.isconnected():
        print('\nConnecting to WiFi...')
        with open('secrets.json') as f:
            secrets = ujson.loads(f.read())
        # List of allowed access points
        acc_pts = secrets['access_points']
        
        # Scan for available access points
        wifis = wlan.scan()
        # sort strongest to weakest signal
        wifis.sort(key=lambda x: x[3], reverse=True)
        
        # Loop through available access points
        for wifi in wifis:
            ssid = wifi[0].decode('utf-8')
            # Is it in list of allowed access points?
            if ssid in acc_pts:
                wlan.connect(ssid, acc_pts[ssid])
                time.sleep(5.0)
                if wlan.isconnected():
                    print('Connected to ' + ssid)
                    print('Network config:', wlan.ifconfig())
                    return 1
                else:
                    continue


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


def main():
    print('\n\n')
    with open('secrets.json') as f:
        secrets = ujson.loads(f.read())
        
    # Turn off access point
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    # Setup WiFi connection.
    wlan = network.WLAN(network.STA_IF)

    print('Ready...')
    while True:
        value = randint(1, 1000)
        if not button.value():
            if not wlan.isconnected():
                wifi_connect(wlan, secrets)
            led.on()
            led2.off()
            p = api_post('test_integer', value)
            led2.on()
            if p == 1:
                led.off()
            
if __name__ == "__main__":
    main()

