# Subscribing the request from DC through broker. Running forever

import paho.mqtt.client as mqtt
import pandas as pd
import datetime
from publish import publish
pd.options.mode.chained_assignment = None
mqtt_host = "54.224.110.254"

def on_connect_mqtt(client, userdata, flags, rc):
    pass
    if rc == mqtt.CONNACK_ACCEPTED:
        # Subscribe to a topic 
        sensors_topic_filter = "request/data"
        client.subscribe(sensors_topic_filter)
def on_subscribe_mqtt(client, userdata, mid, granted_qos):
    print("I've subscribed")

def verify_request():
    # print("in verify")
    df1=pd.read_csv("data/register_dc.csv",delimiter=",",names=["topic","time"])
    df1["time"]=pd.to_datetime(df1["time"],infer_datetime_format=True)
    df2=pd.read_csv("data/data_request.csv",delimiter=",",names=["topic","time"])
    df2["time"]=pd.to_datetime(df2["time"],infer_datetime_format=True)
    l=len(df1)
    for i in range(0,l):
        if(df1["topic"][i]==df2.topic[0]):
            if(df1.time[i] < df2.time[0]):
                df1.time[i]= datetime.datetime.now() # updating the time to the request time
                publish("sensor_data_req","usbdata") # requesting data from sensor
                df1.to_csv("data/register_dc.csv",index=False,header=False)
                with open('data/temporary_store.txt','w') as f:
                    f.write(str(df2.topic[0]))
                f.close()
            df2=df2.drop(df2.index[[0]])
            df2.to_csv("data/data_request.csv",index=False,header=False)
        else:
            pass

def on_message_mqtt(client, userdata, msg):
    mess=msg.payload.decode("utf-8")
    # print(mess)
    with open('data/data_request.csv','a+') as f:
        f.write("\n"+str(mess))
    f.close()
    verify_request()

if __name__ == "__main__":
    mosquitto_client = mqtt.Client(protocol=mqtt.MQTTv311)  # Defining the client
    mosquitto_client.on_connect = on_connect_mqtt
    mosquitto_client.on_subscribe = on_subscribe_mqtt
    mosquitto_client.on_message=on_message_mqtt
    mosquitto_client.connect(host=mqtt_host, port=1883)
    mosquitto_client.loop_forever()

