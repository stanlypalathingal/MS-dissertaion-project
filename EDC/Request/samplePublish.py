import paho.mqtt.publish as pb

pb.single("sensor/payload", "I am payload", 0, False, "mqtt.eclipse.org", 1883)
print("published")