import paho.mqtt.subscribe as sub
import asymcrypt
import paho.mqtt.publish as pb
import datetime as dtm
import sys
import logging
import time

HOST = sys.argv[1]
CONTAINER_MQTT_HOST = sys.argv[2]  # "localhost"  # "3.92.232.55"  # "172.17.0.4"
PORT = 1883
TOPIC = "data/sym_key"
RE_REQ_TOPIC = "request/data"
logging.basicConfig(level=logging.DEBUG)


def encrypt(data):
    cipherTxt = asymcrypt.encrypt_data(data, "deciderPub.pem")
    hexStr = cipherTxt.hex()
    return hexStr


def on_message_print(client, userdata, message):
    if message.topic == "dc1":
        encrypted_data = message.payload.decode()
        new_rnd_bytes = bytes.fromhex(encrypted_data)
        key = asymcrypt.decrypt_data(new_rnd_bytes, "priv.pem")  # Asymm decryption
        logging.info("Got the key and sending to java %s", key.decode("utf-8"))
        pb.single(TOPIC, key, 0, False, CONTAINER_MQTT_HOST, PORT)


if __name__ == "__main__":
    logging.info("Subscription for key started.")
    sub.callback(on_message_print, ["dc1", "sensor/payload"], hostname=HOST, port=PORT)
