#slurry_monitor.py

import paho.mqtt.client as mqtt
import time
mqtt_host = "192.168.119.138"
f=open('/home/stanlysac/Documents/test.csv','a+')
print("Beginning of fle")
def on_connect_mosquitto(client, userdata, flags, rc):
    print("Result from Mosquitto connect: {}".format(
        mqtt.connack_string(rc)))
    # Check whether the result form connect is the CONNACK_ACCEPTED  connack code
    if rc == mqtt.CONNACK_ACCEPTED:
        # Subscribe to a topic filter that provides all the sensors
        sensors_topic_filter = "usbdata"
        print("before subscribe")
        f.close()
        client.subscribe(sensors_topic_filter)
def on_subscribe_mosquitto(client, userdata, mid, granted_qos):
    print("I've subscribed")
    f=open('/home/stanlysac/Documents/test.csv','a+')
def print_received_message_mosquitto(msg):
    print("Message received. Payload: {}".format(str(msg.payload)))

def on_level_message_mosquitto(client, userdata, msg):
    # print_received_message_mosquitto(msg)
    mess=msg.payload.decode("utf-8")
    f.write("\n"+str(mess))
    # with open('/home/pi/Documents/test.csv','a+') as f:
    #     f.write("\n"+str(mess))
    # f.close()

if __name__ == "__main__":
    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mosquitto
    mosquitto_client.on_subscribe = on_subscribe_mosquitto
    print("on message received")
    mosquitto_client.on_message=on_level_message_mosquitto
    print("before connect")
    mosquitto_client.connect(host=mqtt_host, port=1883)
    print("after connect")
    mosquitto_client.loop_forever()
