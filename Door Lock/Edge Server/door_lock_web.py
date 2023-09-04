from door_lock import DoorLock
from paho.mqtt.client import Client
import json

# Handler for RPC messages from web interface
# lock is stored in client userdata
def on_rpc(client, lock, msg):
    data = json.loads(msg.payload)
    lock.set(data["doorlock"])

lock = DoorLock("/dev/ttyACM0", 115200)
client = Client(userdata=lock)

# Connect to web host using access token as username.
client.connect("172.20.10.13")

# Subscribe and set listener for RPC
client.subscribe("/edge_device/action")
client.message_callback_add("/edge_device/action", on_rpc)

client.loop_forever()
