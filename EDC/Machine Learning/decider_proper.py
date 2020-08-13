# Load the packages
import time
import pandas as pd
from pymongo import MongoClient
from sklearn.tree import DecisionTreeClassifier
import warnings
from client import subscribeStatus  #client.py for collecting the socket message
import sys
import logging
import datetime

# Mongodb connection
mongo_host = sys.argv[2]
client = MongoClient(mongo_host, 27017)
IoTClient = client['test']
IoTDB = IoTClient["IoT"]
IoTColl = IoTDB["sensorData"]

logging.basicConfig(level=logging.DEBUG)
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

# load the files of list of sensors, units,types and key. All the files are in data folder
list_sensor = pd.read_csv("data/list_sensor1.csv", delimiter=",", names=["id", "factor"])
list_units = pd.read_csv("data/list_units1.csv", delimiter=",", names=["id", "factor"])
list_type = pd.read_csv("data/list_types1.csv", delimiter=",", names=["id", "factor"])

# load the training dataset
df = pd.read_csv("data/training_data.csv")
total_row = df.shape[0]
trial_row = int(total_row - (total_row * 0.25))

# Function1
# function to factor the columns of sensor,types and units
def factorize(obj, obj_list, table, data, write_to_file):
    if (write_to_file):
        data_s = pd.DataFrame(data[obj].unique())
        new_sensor = data_s[~data_s[0].isin(obj_list.id)]
        ns = []
        if (len(new_sensor) > 0):
            l = len(obj_list)
            for s in new_sensor[0]:
                n = [s, l]
                l = l + 1
                ns.append(n)
            ns = pd.DataFrame(ns, columns=["id", "factor"])
            ns.to_csv(table, mode='a', header=False, index=False)

    obj_list = pd.read_csv(table, delimiter=",", names=["id", "factor"])
    l = len(obj_list)
    for i in range(0, l):
        if (len(data.loc[data[obj] == obj_list.id[i]]) > 0):
            data.loc[data[obj] == obj_list.id[i], obj] = obj_list.factor[i]

'''
function call has 4 parameters,
	First is the name of the column (sensor,type,units) as in the dataframe
	Second is the variable containing the list of sensors loaded from file.
	Third is the file name from where it was loaded earlier and will be stored.
	Fourth is the name of the dataframe
	Fifth is to find whether it is for train or test. Only during train the files are written to csv
		It is passed as boolean
'''
factorize('Sensor', list_sensor, 'data/list_sensor1.csv', df, True)
factorize('Type', list_type, 'data/list_types1.csv', df, True)
factorize('Units', list_units, 'data/list_units1.csv', df, True)

# factorise flags
df.loc[df['Flag'] == False, 'Flag'] = 0
df.loc[df['Flag'] == True, 'Flag'] = 1

'''
assign the x and y where
	x is the predictor(independent)
	y is predicted (dependent)
'''
x = ['Sensor', 'Type', 'Units', 'Value']
y = ['Flag']

# split the train and test datasets
train = df.loc[1:trial_row, ]
test = df.loc[trial_row + 1:total_row, ]

# create the datasets to apply machine learning
x_train, y_train, x_test, y_test = train[x], train[y], test[x], test[y]

# Decision Tree algorithm
decision = DecisionTreeClassifier().fit(x_train, y_train)
decision_yhat = decision.predict(x_test)

# Add this any where in the decider_proper.py
def check(a, df2):
    if (a <= 19.0):
        if (df2.loc[df2.type == "Temperature"].status.to_numpy() == 1):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 1
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 2):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 2
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 3):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 3
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 4):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 4
        else:
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy()
    if (a >= 20.0 and a < 25.0):
        if (df2.loc[df2.type == "Temperature"].status.to_numpy() == 0):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 1
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 2):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 1
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 3):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 2
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 4):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 3
        else:
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy()
    if (a >= 25.0 and a < 30.0):
        if (df2.loc[df2.type == "Temperature"].status.to_numpy() == 0):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 2
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 1):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 1
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 3):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 1
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 4):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 2
        else:
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy()
    if (a >= 30.0 and a < 35.0):
        if (df2.loc[df2.type == "Temperature"].status.to_numpy() == 0):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 3
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 1):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 2
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 2):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 1
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 4):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() - 1
        else:
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy()
    if (a >= 35.0 and a < 40.0):
        if (df2.loc[df2.type == "Temperature"].status.to_numpy() == 0):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 4
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 1):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 3
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 2):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 2
        elif (df2.loc[df2.type == "Temperature"].status.to_numpy() == 3):
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy() + 1
        else:
            df2.loc[df2.type == "Temperature", "status"] = df2.loc[df2.type == "Temperature"].status.to_numpy()
    if (a >= 40.0):
        df2.loc[df2.type=="Temperature","status"]=4   
        logging.info("Publish Danger")
    df2.loc[df2.type == "Temperature", "max1"] = a
    return df2.loc[df2.type == "Temperature"]

'''
The while lop below is infinite.
First it will call the function subcribeKey() from the subscribe_key file. This file looks for
	a key. It will collect the key and will save in a text file.
It will look for an entry in the key file and will be called new key.
It will compare with the old key stored earlier and
	if they are different it will enter into the if loop
'''
while (True):
    mess = subscribeStatus() # collect the socket message
    if (mess == "done"):
        start = time.time()
        temp_data1 = pd.read_csv("data/test.csv", delimiter=",",
                                 names=["Sensor", "Type", "Units", "time", "Value", "Flag"]) # the original data to DB if everything is fine
        if(temp_data1.shape[0]>0):
            temp_data = pd.read_csv("data/test.csv", delimiter=",",
                                    names=["Sensor", "Type", "Units", "time", "Value", "Flag"])
            temp_data = temp_data.drop_duplicates()
            logging.info("Number of rows for testing %d", temp_data.shape[0])
            factorize('Sensor', list_sensor, 'data/list_sensor1.csv', temp_data, False)
            factorize('Type', list_type, 'data/list_types1.csv', temp_data, False)
            factorize('Units', list_units, 'data/list_units1.csv', temp_data, False)

            temp_test = temp_data[x]

            decision_yhat = decision.predict(temp_test)
            flagged_false = (decision_yhat == 0).sum()
            flagged_true = (decision_yhat == 1).sum()

            test_acc = 100 - (flagged_true / flagged_false)
            logging.info("Amount of true readings are %f", test_acc)

            # Checking the accuracy
            if (test_acc > 99.00):
                end = time.time()
                timeTaken = end - start
                logging.info("Time taken for ML accuracy and Mongo insertion %f", timeTaken)

                # timeframe analysis algorithm
                df_max = pd.read_csv("data/sensormax.csv", names=["sensor", "type", "max1", "status"])
                df_sensor = temp_data1.Sensor.unique()
                for j in range(0, len(df_sensor)):
                    df1 = temp_data1.loc[temp_data1.Sensor == df_sensor[j]]
                    a = max(df1.loc[df1.Type == "Temperature"].Value)
                    new = check(a, df_max.loc[df_max.sensor == df_sensor[j]])
                    df_max = df_max.drop(df_max.loc[df_max.sensor==df_sensor[j]].index,axis=0)
                    df_max = df_max.append(new)
                df_max.to_csv("data/sensormax.csv",mode="w",index=False,header=False)
                df_max = pd.read_csv("data/sensormax.csv", names=["sensor", "type", "max1", "status"])
                logging.info(df_max)

                # clear the contents of the file for next set of data
                f = open("data/test.csv", "w")
                f.truncate()
                f.close()

                # Insert the data to DB
                IoTColl.insert_many(temp_data1.to_dict("records"))

                end1 = time.time()
                timeTaken1 = end1 - start
                logging.info("Time for final analysis %f", timeTaken1)
            else:
                logging.info("Accuracy is below 99.00% and no insertion in mongodb")

                # clear the contents of the file for next set of data
                f = open("data/test.csv", "w")
                f.truncate()
                f.close()
                end = time.time()
                timeTaken = end - start
                logging.info("Time taken %f", timeTaken)
            
            # final benchmarking
            a = open('data/bench_time.txt').read().replace('\n', '')
            a = pd.to_datetime(a, infer_datetime_format=True)
            c = (datetime.datetime.now() - a)
            logging.info("Time taken for benchmark %f", c.total_seconds())
