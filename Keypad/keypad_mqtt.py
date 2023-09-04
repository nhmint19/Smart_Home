from keypad import KeyPad
from paho.mqtt.client import Client
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
def on_message(client, userdata, msg):
    print 'Topic: ' + msg.topic + '\nMessage: ' + msg.payload

keypad = KeyPad("/dev/ttyS0", 9600)
client = Client(userdata=keypad)
client.loop_start()

# client connect
client.on_connect = on_connect

# client receive message
client.on_message = on_message

# set up credentials for thingsboard
client.username_pw_set("9HR7OciX9vSmYfknZ88x")
client.connect("172.20.10.9", 1883, 60)

request = {
    "method": "getKeypad",
    "params": {"Keypad": ""}
}
# subscribe to receive response after making request
client.subscribe('v1/devices/me/rpc/response/+')

try:
    while True:
        request["params"]["Keypad"] = keypad.state() # get keypad's state
        # making request to thingsboard
        client.publish('v1/devices/me/rpc/request/1', json.dumps(request), 1) 
except KeyboardInterrupt:
    pass

client.loop_stop()
print('disconnect')
client.disconnect()