# For the registration of the public key from the DC
# Subscription
import paho.mqtt.client as mqtt
mqtt_host = "mqtt.eclipse.org"

def on_connect_mqtt(client, userdata, flags, rc):
    pass
    if rc == mqtt.CONNACK_ACCEPTED:
        sensors_topic_filter = "request/register"
        client.subscribe(sensors_topic_filter)
def on_subscribe_mqtt(client, userdata, mid, granted_qos):
    print("I've subscribed")

def on_message_mqtt(client, userdata, msg):
    mess=msg.payload.decode("utf-8")
    with open('data/register_dc.csv','a+') as f:
        f.write("\n"+str(mess))
    f.close()
    
if __name__ == "__main__":
    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mqtt
    mosquitto_client.on_subscribe = on_subscribe_mqtt
    mosquitto_client.on_message=on_message_mqtt
    mosquitto_client.connect(host=mqtt_host, port=1883)
    mosquitto_client.loop_forever()
