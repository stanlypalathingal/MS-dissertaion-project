#!/bin/bash
# Program with while loop
import time
import paho.mqtt.client as mqtt
start=time.time()
end=time.time()

print("starting of the program ",end-start)
import pandas as pd
# import numpy as np

from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

end=time.time()
print("loading of the packagaes ", end-start)

list_sensor=pd.read_csv("data/list_sensor1.csv", delimiter=",",names=["id","factor"])
list_units=pd.read_csv("data/list_units1.csv", delimiter=",",names=["id","factor"]) 
list_type=pd.read_csv("data/list_types1.csv", delimiter=",",names=["id","factor"]) 

df=pd.read_csv("data/Sample dataset values1.csv")
df.head(3)
df.shape
total_row=df.shape[0]
trial_row=int(total_row-(total_row*0.25))
print("total rows")
print(trial_row)

# df=pd.read_csv("data/Sample dataset values.txt")

def factorize(obj,obj_list,table,data):
    data_s=pd.DataFrame(data[obj].unique())
    
    new_sensor = data_s[~data_s[0].isin(obj_list.id)]
    ns=[]
    if(len(new_sensor)>0):
        l=len(obj_list)
        for s in new_sensor[0]:
            n=[s,l]
            l=l+1
            ns.append(n)
        ns=pd.DataFrame(ns,columns=["id","factor"])
        ns.to_csv(table,mode='a', header=False,index=False)

    obj_list=pd.read_csv(table,delimiter=",",names=["id","factor"])
    l=len(obj_list)
    for i in range(0,l):
        data.loc[data[obj]==obj_list.id[i],obj]=obj_list.factor[i]

print("location 1")
factorize('Sensor',list_sensor,'data/list_sensor1.csv',df)
print("location 2")
factorize('Type',list_type,'data/list_types1.csv',df)
print("location 3")
factorize('Units',list_units,'data/list_units1.csv',df)

df.loc[df['Flag']==False,'Flag']=0
df.loc[df['Flag']==True,'Flag']=1

x= ['Sensor', 'Type', 'Units','Value']
y=['Flag']

train=df.loc[1:trial_row,]
test=df.loc[trial_row+1:total_row,]
print("size of train ",train.shape[0])
print("size of test ", test.shape[0])

print("counts of 0 and 1")
print(train['Flag'].value_counts())
print(test['Flag'].value_counts())

x_train,y_train,x_test,y_test = train[x],train[y],test[x],test[y]

end=time.time()
print("Completion of data preparation ", end-start)

#confusion Matrix
def ConfusionMatrix(x,y):
    a = confusion_matrix(x,y)
    print(a)
    # b = (a[0][0]+a[1][1])/(a[1][1]+a[0][1]+a[0][0]+a[1][0])
    # return round(b*100,2)

#Decision Tree
decision = DecisionTreeClassifier().fit(x_train,y_train)
decision_yhat = decision.predict(x_test)

print(decision.score(x_test,y_test))

print("counts of 0 and 1")
print("zeros",(decision_yhat == 0).sum())
print("ones",(decision_yhat == 1).sum())

decision_acc= ConfusionMatrix(decision_yhat,y_test)
print(decision_acc)

end=time.time()
print("before calling the function", end-start)


# function for publish
def result(option):
	def on_connect(client, userdata, flags, rc):
		print("Result from connect: {}".format(mqtt.connack_string(rc)))
		# Check whether the result form connect is the CONNACK_ACCEPTED connack code
		if rc != mqtt.CONNACK_ACCEPTED:
			raise IOError("Couldn't establish a connection with the MQTT server")
	def publish_value(client, topic, value):
		result = client.publish(topic=topic, payload=value, qos=1)
		print("Result from connect:" )
		print(value)
		return result
	if __name__ == "__main__":
		client = mqtt.Client(protocol=mqtt.MQTTv311)
		client.on_connect = on_connect
		client.connect(host="mqtt.eclipse.org", port=1883)
		client.loop_start()
		topic="result"
		value=option
		publish_value(client,topic, value)
		client.disconnect()
		client.loop_stop()
	
a=True
while(a):
	start=time.time()
	end=time.time()
	print("before calling the function in while", end-start)
	
	temp_data=pd.read_csv("/home/pi/Documents/test1.csv",delimiter=",", 
	names=["packet_no","Sensor","Type","Units","time","Flag","Value","Key"])
	print(temp_data.shape[0])
	end=time.time()
	print("before removing duplicates  in while", end-start)
	temp_data=temp_data.drop_duplicates()
	print(temp_data.shape[0])

	if(temp_data.shape[0]>0):

		factorize('Sensor',list_sensor,'data/list_sensor1.csv',temp_data)
		factorize('Type',list_type,'data/list_types1.csv',temp_data)
		factorize('Units',list_units,'data/list_units1.csv',temp_data)
		print("size of the dataset : ",temp_data.shape[0])
		
		temp_test= temp_data[x]
		print("the columns are ",temp_test.columns)
		
		decision_yhat = decision.predict(temp_test)
		print("counts of 0 and 1")
		print("zeros",(decision_yhat == 0).sum())
		print("ones",(decision_yhat == 1).sum())
		
		temp_test_y=temp_data[y]
		decision_acc= ConfusionMatrix(decision_yhat,temp_test_y)
		print(decision_acc)
		
		result("proceed")

	else:
		print("There are no values in the dataset ",temp_data.shape[0])
		
	end=time.time()
	print("before calling the function", end-start)

	#time.sleep(70)
	a=False
#print(data.head())

