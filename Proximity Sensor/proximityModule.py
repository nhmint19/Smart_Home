import serial
import paho.mqtt.client as mqtt
import json
    
arduino = serial.Serial('/dev/ttyS0', 9600)
THINGSBOARD_HOST = "172.20.10.9"
#ACCESS_TOKEN = "Vjg6cmwH7AIQXQGbQaXN"
ACCESS_TOKEN = "VKu7V8pNhBkpHfhR8uvN"
WEBSERVER = "172.20.10.13"

sensor_data = {'distance': 0, 'activity': 0}

def on_message(client, userdata, msg):
    print("CALIBRATING...")
    arduino.write(b"calibrate")

def main():
    blacklistedStrings = ["Pass", "Calibrating"]
    activity = 0
    
    client = mqtt.Client()
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(THINGSBOARD_HOST, 1883, 60)
    #client.connect(WEBSERVER, 1883, 60)
    
    client.loop_start()
    
    client.subscribe("v1/devices/me/rpc/request/+")
    client.message_callback_add("v1/devices/me/rpc/request/+", on_message) #Thingsboard
    
    while True:
        line = str(arduino.readline()).strip("b'\\r\\n'")
        
        #Wait until calibration is over
        if not any(x in line for x in blacklistedStrings): 
            lineArray = line.split(" ")
    
            distance = int(lineArray[1])               
            activity = int(lineArray[4])
            
            print(line)
                
            sensor_data['distance'] = distance
            sensor_data['activity'] = activity
                
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1) #Send to Thingsboard
            #client.publish('/edge_device/ultrasonic', distance, 1) #Send to webserver

            
        else:
            print(line)
            
    client.loop_stop()
                 
if __name__ == "__main__":
    main()
