import paho.mqtt.publish as pb
import time as tm
import datetime as dtm

HOST = "mqtt.eclipse.org"
PORT = 1883


def publishData(i):
    TOPIC = "sensor/payload"
    regPayload = "dc1" + "," + str(dtm.datetime.now())
    pb.single(TOPIC, regPayload, 0, False, HOST, PORT)
    print("Batch:", i, "-Request initiated under topic 'request/data'")
    tm.sleep(10)


def startProcess():
    i = 0
    while True:
        i = i + 1
        publishData(i)


if __name__ == "__main__":
    startProcess()
