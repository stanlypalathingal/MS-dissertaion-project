import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    # print("Result from connect: {}".format(mqtt.connack_string(rc)))
    # Check whether the result form connect is the CONNACK_ACCEPTED connack code
    if rc != mqtt.CONNACK_ACCEPTED:
        raise IOError("Couldn't establish a connection with the MQTT server")
def publish_value(client, topic, value):
    client.publish(topic=topic, payload=value, qos=1,retain=True)
    # print("Result from connect:" )

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.connect(host="mqtt.eclipse.org", port=1883)
client.loop_start()
topic="symkey"
value="sdfg4fshwstrsjdghmdytmjhyktdidnhcghmhcydtkmkhgdfjtur"
publish_value(client,topic, value)
client.disconnect()
client.loop_stop()