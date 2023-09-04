from door_lock import DoorLock
from paho.mqtt.client import Client
import json

# Handler for RPC messages from ThingsBoard
# lock is stored in client userdata
def on_rpc(client, lock, msg):
    data = json.loads(msg.payload)
    if data["method"] == "setLocked":
        lock.set(data["params"])
    elif data["method"] == "getLocked":
        client.publish(msg.topic.replace("request", "response"), json.dumps(lock.state()))

lock = DoorLock("/dev/ttyACM0", 115200)
client = Client(userdata=lock)

# Connect to ThingsBoard host using access token as username.
client.username_pw_set("w31L3qQpLhbsfUGTwrWQ")
client.connect("172.20.10.13")

# Subscribe and set listener for RPC
client.subscribe("v1/devices/me/rpc/request/+")
client.message_callback_add("v1/devices/me/rpc/request/+", on_rpc)

client.loop_forever()
