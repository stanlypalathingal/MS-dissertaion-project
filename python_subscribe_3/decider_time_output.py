#!/bin/bash

# Load the publish and subscribe files
from publish import *
from subscribe_key import *

#Load the packages
import time
start=time.time()
end=time.time()

print("starting of the program ",end-start)
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

end=time.time()
print("loading of the packagaes ", end-start)

#load the files of list of sensors, units,types and key. All the files are in data folder
list_sensor=pd.read_csv("data/list_sensor1.csv", delimiter=",",names=["id","factor"])
list_units=pd.read_csv("data/list_units1.csv", delimiter=",",names=["id","factor"]) 
list_type=pd.read_csv("data/list_types1.csv", delimiter=",",names=["id","factor"]) 
old_key=open('data/key.txt').readlines()
old_key = ''.join(old_key)
# print(old_key)

#load the training dataset
df=pd.read_csv("data/Sample dataset values1.csv")
df.head(3)
df.shape
total_row=df.shape[0]
trial_row=int(total_row-(total_row*0.25))
print("total rows")
print(trial_row)

#function to factor the columns of sensor,types and units
def factorize(obj,obj_list,table,data):
#     print(data[obj].unique())
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

'''
function call has 4 parameters, 
	First is the name of the column (sensor,type,units) as in the dataframe
	Second is the variable containing the list of sensors loaded from file. 
	Third is the file name from where it was loaded earlier and will be stored. 
	Fourth is the name of the dataframe
'''
factorize('Sensor',list_sensor,'data/list_sensor1.csv',df)
factorize('Type',list_type,'data/list_types1.csv',df)
factorize('Units',list_units,'data/list_units1.csv',df)

#factorise flags
df.loc[df['Flag']==False,'Flag']=0
df.loc[df['Flag']==True,'Flag']=1

'''
assign the x and y where
	x is the predictor(independent) 
	y is predicted (dependent)
'''
x= ['Sensor', 'Type', 'Units','Value']
y=['Flag']

#split the train and test datasets
train=df.loc[1:trial_row,]
test=df.loc[trial_row+1:total_row,]
print("size of train ",train.shape[0])
print("size of test ", test.shape[0])

print("counts of 0 and 1")
print(train['Flag'].value_counts())
print(test['Flag'].value_counts())

#create the datasets to apply machine learning
x_train,y_train,x_test,y_test = train[x],train[y],test[x],test[y]

end=time.time()
print("Completion of data preparation ", end-start)

#confusion Matrix
def ConfusionMatrix(x,y):
    a = confusion_matrix(x,y)
    print(a)
    b = (a[0][0]+a[1][1])/(a[1][1]+a[0][1]+a[0][0]+a[1][0])
    return round(b*100,2)

#Decision Tree algorithm
decision = DecisionTreeClassifier().fit(x_train,y_train)
decision_yhat = decision.predict(x_test)

print(decision.score(x_test,y_test))

print("counts of 0 and 1")
print("zeros",(decision_yhat == 0).sum())
print("ones",(decision_yhat == 1).sum())

end=time.time()
print("before calling the function", end-start)

decision_acc= ConfusionMatrix(decision_yhat,y_test)
print(decision_acc)

end=time.time()
print("before calling the function", end-start)

'''
The while lop below is infinite. 
First it will call the function sunscribeKey() from the subscribe_key file. This file looks for
	a key. It will collect the key and will save in a text file.
It will look for an entry in the key file and will be called new key. 
It will compare with the old key stored earlier and 
	if they are different it will enter into the if loop  
'''	
while(True):
	subscribeKey() # call to subscrive_key.py
	new_key=open('data/key.txt').readlines()
	new_key = ''.join(new_key)

	if((old_key!=new_key)):
		print("startin the analysis")
		start=time.time()
		#load the data for testing and remove the dulicates
		temp_data=pd.read_csv("/home/stanlysac/Documents/test.csv",delimiter=",", 
			names=["Sensor","Type","Units","time","Flag","Value"])
		print(temp_data.shape[0])
		temp_data=temp_data.drop_duplicates()
		print(temp_data.shape[0])

		#call hte function to factorise
		factorize('Sensor',list_sensor,'data/list_sensor1.csv',temp_data)
		factorize('Type',list_type,'data/list_types1.csv',temp_data)
		factorize('Units',list_units,'data/list_units1.csv',temp_data)
		
		temp_test= temp_data[x]
		decision_yhat = decision.predict(temp_test)
		print("counts of 0 and 1")
		print("zeros",(decision_yhat == 0).sum())
		print("ones",(decision_yhat == 1).sum())
		
		# temp_test_y=temp_data[y]
		# decision_acc= ConfusionMatrix(decision_yhat,temp_test_y)
		print(decision_acc)

		# the function below publishes the decision back through publish
		publishResult("proceed")
		# f = open("/home/stanlysac/Documents/test.csv", "w")
		# f.truncate()
		# f.close()
		
		#assigning newkey with old key 
		old_key=new_key
		end=time.time()
		print("before calling the function", end-start)
	
	# else:
	# 	print("There are no values in the dataset ",temp_data.shape[0])
		

