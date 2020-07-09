import time

# Load the publish and subscribe files
from sym_key_generator import sym_key
from client import subscribeStatus
from publish import publish
from sym_key_generator import encrypt_public

# Load the packages
import datetime
import pandas as pd
# load the training dataset
df = pd.read_csv("data/training_data.csv")

# the original combination of sensor, type and units
a = df.groupby(["Sensor", "Type", "Units"])["Sensor"].unique().to_frame(name="1").reset_index()
original_combination = a.drop("1", 1)

# Function 1
'''
accepts two parameters.
    First is the dataframe of combinations of original dataset
    second is the test dataset
It then uses the group by to create the combinations
Both are merged using the inner. So it will have the common ones in original and test
Combine the new (c) with that of test (b).
use duplicates only to keep the differnces
'''

def spoof_detect(a, b):
    c = (b.merge(a, how="inner"))
    fake = pd.concat([c, b], sort=False)
    # print(fake)
    # print(fake.drop_duplicates(keep=False))
    return fake.drop_duplicates(keep=False)

'''
assign the x and y where
	x is the predictor(independent)
	y is predicted (dependent)
'''
x = ['Sensor', 'Type', 'Units', 'Value']
y = ['Flag']

# function for finding the time duration
def benchmark(name_of_dc):
	df1 = pd.read_csv("data/register_dc.csv", delimiter=",",names=["topic", "time"])
	df1["time"] = pd.to_datetime(df1["time"], infer_datetime_format=True)
	a = (df1.loc[df1.topic == name_of_dc, "time"].iloc[0])
	c = (datetime.datetime.now()-a)
	print("Time taken benchmark ",c.total_seconds())
	print("*************************************************")

# funtion for log files
def abort_reason(file,reason):
	text_file = open("/home/pi/Documents/"+file+".log", "a+") 
	text_file.write("\n"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+","+ reason) # write the time and reason
	text_file.close()
	# print("/home/pi/Documents/"+file+".log"+ reason)

# function for clearing files
def clearFiles():
	f = open("data/test.csv", "w")
	f.truncate()
	f.close()

def abort_process(original_combination,temp_data,start):
	publish("sensor_sym_key","abort")
	encrypt_public("nodata")
	benchmark(name_of_dc)
	abort_reason("error"," \n")
	spoof_detect(original_combination,temp_data).to_csv("/home/pi/Documents/error.log",mode="a",index=False) # save the error details with time
	end=time.time()
	print("Time taken for the analysis after receving the data ",end-start)
	clearFiles()

'''
The while lop below is infinite.
First it will call the function sunscribeKey() from the subscribe_key file. This file looks for
	a key. It will collect the key and will save in a text file.
It will look for an entry in the key file and will be called new key.
It will compare with the old key stored earlier and
	if they are different it will enter into the if loop
'''
while(True):
	mess=subscribeStatus()
	if(mess=="done"):
		start=time.time()
		#print("starting the analysis")
		name_of_dc=open('data/temporary_store.txt').read().replace('\n','')
		#load the data for testing and remove the dulicates
		temp_data=pd.read_csv("data/test.csv",delimiter=",",names=["Sensor","Type","Units","time","Flag","Value"])
		b=temp_data.groupby(["Sensor","Type","Units"])["Sensor"].unique().to_frame(name="1").reset_index().drop("1",1)
		if(temp_data.shape[0]>0):
			temp_data=temp_data.drop_duplicates()
			print("Number of rows for testing",temp_data.shape[0])
			# Checking  the existance of dummy or spoof data
			if(len(spoof_detect(a[["Sensor"]],b[["Sensor"]]))==0):
				print("The sensors are all authentic")
				if(len(spoof_detect(a[["Sensor","Type"]],b[["Sensor","Type"]]))==0):
					print("The categories are all authentic")
					if(len(spoof_detect(a[["Sensor","Type","Units"]],b[["Sensor","Type","Units"]]))==0):
						print("The units are all authentic")
					else:
						print("there are fake units")
						abort_process(a,b,start)
				else:
					print("there are fake categories")
					abort_process(a,b,start)
			else:
				print("there are fake sensors")
				abort_process(a,b,start)

		else:
			# publish(name_of_dc,"nodata")
			# publish("sensor_sym_key","abort")
			# encrypt_public("nodata")
			print("nodata")
			benchmark(name_of_dc)
			abort_reason("no_data","no data available in the sensors")
			clearFiles()
		
		mess=None

