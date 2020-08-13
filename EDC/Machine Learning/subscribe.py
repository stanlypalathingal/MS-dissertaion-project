# Subscribing the data  from broker. Running forever
import paho.mqtt.client as mqtt
import socket
import subprocess as sub
import sys
import threading
import logging

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 9009))
s.listen()
mqtt_host = sys.argv[1]
mongo_host = sys.argv[2]

logging.basicConfig(level=logging.DEBUG)


# Main thread will call Child thread and runs the decider_proper.py
class decider(threading.Thread):
    def run(self):
        sub.call(["python", "decider_proper.py", mqtt_host, mongo_host])


class benchmark(threading.Thread):
    def run(self):
        sub.call(["python", "bench_subscribe.py", mqtt_host])


def on_connect_mqtt(client, userdata, flags, rc):
    pass
    if rc == mqtt.CONNACK_ACCEPTED:
        # client.subscribe("machine_learning")
        client.subscribe("machine_learning") # subscribe topic

def on_subscribe_mqtt(client, userdata, mid, granted_qos):
    logging.info("I've subscribed sensor Data")

def on_message_mqtt(client, userdata, msg):
    mess = msg.payload.decode("utf-8")
    with open('data/test.csv', 'a+') as f:
        if (mess == "done"):
            logging.info("done")
            clientsocket, address = s.accept()
            clientsocket.send(bytes("done", "utf-8")) # informs the completion of the data collection
            mess = ""
            mosquitto_client.connect(host=mqtt_host, port=1883)
        f.write("\n" + str(mess))
    f.close()


if __name__ == "__main__":
    DeciderObj = decider()
    DeciderObj.start()  # will execute the child thread for decider_proper.py

    Benchmark = benchmark()
    Benchmark.start()  # Will execute the child thread for benchmark_subscribe.py

    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mqtt
    mosquitto_client.on_subscribe = on_subscribe_mqtt
    mosquitto_client.on_message = on_message_mqtt
    mosquitto_client.connect(host=mqtt_host, port=1883)
    mosquitto_client.loop_forever()
