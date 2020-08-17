import paho.mqtt.publish as pb
import time as tm
import datetime as dtm
from subprocess import call
import threading
import sys
import logging
import asymcrypt

HOST = sys.argv[1]
CONTAINER_MQTT_HOST = sys.argv[2]
PORT = 1883
logging.basicConfig(level=logging.DEBUG)


class subscribe(threading.Thread):
    def run(self):
        call(["python", "Subscribe.py", HOST, CONTAINER_MQTT_HOST])


class publish:
    def publishData(self, i):
        TOPIC = "request/data"
        regPayload = self.encrypt("dc1" + "," + str(dtm.datetime.now()))
        pb.single(TOPIC, regPayload, 0, False, HOST, PORT)
        pb.single("bench_subscribe", str(dtm.datetime.now()), 0, False, CONTAINER_MQTT_HOST, PORT)
        logging.info("Batch: %s -Request initiated under topic 'request/data'", i)
        sleep_Time = int(sys.argv[3])
        tm.sleep(sleep_Time)

    def encrypt(self, data):
        cipherTxt = asymcrypt.encrypt_data(data, "deciderPub.pem")
        hexStr = cipherTxt.hex()
        return hexStr

    def startProcess(self):
        i = 0
        while True:
            i = i + 1
            self.publishData(i)


if __name__ == "__main__":
    logging.info("External broker ip set to : " + sys.argv[1])
    logging.info("Internal broker ip set to : " + sys.argv[2])
    logging.info("Sleep time set to : " + sys.argv[3])
    subs = subscribe()
    subs.start()  # Initiates a new thread to run subscribe.py
    pub = publish()  # object creation for publish class
    pub.startProcess()
