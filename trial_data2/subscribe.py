#slurry_monitor.py

import paho.mqtt.client as mqtt
import time
import json
mqtt_host = "mqtt.eclipse.org"

def on_connect_mosquitto(client, userdata, flags, rc):
    print("Result from Mosquitto connect: {}".format(
        mqtt.connack_string(rc)))
    # Check whether the result form connect is the CONNACK_ACCEPTED  connack code
    if rc == mqtt.CONNACK_ACCEPTED:
        # Subscribe to a topic filter that provides all the sensors
        sensors_topic_filter = "usbdata"
        client.subscribe(sensors_topic_filter)
def on_subscribe_mosquitto(client, userdata, mid, granted_qos):
    print("I've subscribed")
def print_received_message_mosquitto(msg):
    print("Message received. Payload: {}".format(str(msg.payload)))

def on_level_message_mosquitto(client, userdata, msg):
    print_received_message_mosquitto(msg)
    mess=msg.payload.decode("utf-8")
    with open('/home/pi/Documents/test.csv','a+') as f:
        f.write("\n"+str(mess))
    f.close()

if __name__ == "__main__":
    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mosquitto
    mosquitto_client.on_subscribe = on_subscribe_mosquitto
    mosquitto_client.on_message=on_level_message_mosquitto
    
    mosquitto_client.connect(host=mqtt_host, port=1883)
    mosquitto_client.loop_forever()
