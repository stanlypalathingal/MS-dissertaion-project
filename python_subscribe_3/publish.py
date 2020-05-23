import paho.mqtt.client as mqtt

def publishResult(option):
    def on_connect(client, userdata, flags, rc):
        # print("Result from connect: {}".format(mqtt.connack_string(rc)))
        # Check whether the result form connect is the CONNACK_ACCEPTED connack code
        if rc != mqtt.CONNACK_ACCEPTED:
            raise IOError("Couldn't establish a connection with the MQTT server")
    def publish_value(client, topic, value):
        result = client.publish(topic=topic, payload=value, qos=1)
        print("Decision is to ",value, " and data is publised back to the sensor")
        return result

    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.connect(host="mqtt.eclipse.org", port=1883)
    client.loop_start()
    topic="usbresult"
    value=option
    publish_value(client,topic, value)
    client.disconnect()
    client.loop_stop()