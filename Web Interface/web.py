import pymysql
import json
from paho.mqtt.client import Client
from flask import Flask, render_template, redirect

app = Flask(__name__)

data = {
    "ultrasonic_value":'0',
    "doorlock": '0',
} 

IP_ADDRESS = "127.0.0.1"

# Fetch ultrasonic data and state from db
def fetch_data():
    dbConn = pymysql.connect("localhost", "pi", "", "smarthome") or die("Could not connect to database")
    with dbConn:
        # get sensor data
        cursor = dbConn.cursor()
        cursor.execute("SELECT * from ultrasonic")
        dbConn.commit()
        result_ultrasonic = cursor.fetchall()
        data["ultrasonic_value"] = result_ultrasonic[-1][0]
        
        # get states
        cursor.execute("SELECT doorlock from state where id = 1")
        dbConn.commit()
        result_states = cursor.fetchone()
        data["doorlock"] = result_states[0]
        
        cursor.close()
 
# On connect to devices through mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # subscribe to these topic to get updated data
    client.subscribe([("/edge_device/ultrasonic", 1),("/edge_device/doorlock", 1)])

# On receiving messages 
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    dbConn = pymysql.connect("localhost", "pi", "", "smarthome") or die("Could not connect to database")
    with dbConn:
        cursor = dbConn.cursor()
        if (msg.topic == "/edge_device/ultrasonic"):
            cursor.execute("INSERT INTO ultrasonic (data) VALUES (%s)", (msg.payload))
        if (msg.topic == "/edge_device/doorlock"):
            cursor.execute("UPDATE state SET doorlock = (%s) WHERE id = 1", (json.loads(msg.payload)["params"]["doorlock"]))
        dbConn.commit()
        cursor.close()

# Main web page
@app.route('/')
def index():
    fetch_data()
    # Pass the template data to index.html
    return render_template('index.html', **data)

# Show data
@app.route('/ultrasonic_data')
def show_data():
    dbConn = pymysql.connect("localhost", "pi", "", "smarthome") or die("Could not connect to database")
    with dbConn:
        # get sensor data
        cursor = dbConn.cursor()
        cursor.execute("SELECT * from ultrasonic order by id DESC")
        dbConn.commit()
        ultrasonic_data = {
            "data": cursor.fetchall()
        }
        cursor.close()
    # Pass the template data to index.html
    return render_template('data.html', **ultrasonic_data)

# Graph page
@app.route('/graph')
def show_graph():
    dbConn = pymysql.connect("localhost", "pi", "", "smarthome") or die("Could not connect to database")
    with dbConn:
        # get sensor data
        cursor = dbConn.cursor()
        cursor.execute("SELECT * from ultrasonic order by id desc limit 10")
        dbConn.commit()
        ultrasonic_result = cursor.fetchall()[::-1]
        ultrasonic_data = {
            "label": list(map(lambda x: x[2], ultrasonic_result)),
            "data": list(map(lambda x: x[1], ultrasonic_result))
        }
        cursor.close()

    # Pass the template data to index.html
    return render_template('graph.html', **ultrasonic_data)
# Function to control door lock manually
@app.route("/<action>")
def action(action):
    fetch_data()
    key = ""
    val = ""
    if action == 'lock_on':
        data["doorlock"] = '1'
        key = "doorlock"
        val = "1"
    if action == 'lock_off':
        data["doorlock"] = '0'
        key = "doorlock"
        val = "0"
        
    # update data to the local database
    if (key != "" and val != ""):
        dbConn = pymysql.connect("localhost", "pi", "", "smarthome") or die("Could not connect to database")
        with dbConn:
            cursor = dbConn.cursor()
            cursor.execute("UPDATE state SET " + key + " = " + val + " WHERE id = 1")
            dbConn.commit()
            cursor.close()
            
        # publish the updated data to devices
        client.publish("/edge_device/action", json.dumps(data), 1)

    # Redirect to the index path
    return redirect("/")

if __name__ == "__main__":
    # initialize the client for mqtt
    client = Client()
    client.loop_start()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(IP_ADDRESS, 1883, 60)
    app.run(host='0.0.0.0', port = 80, debug = True)
    
    # end the connection between client and broker
    client.loop_stop()
    client.disconnect()