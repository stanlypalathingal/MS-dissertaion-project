import time
start = time.time()

# Load the publish and subscribe files
from sym_key_generator import sym_key
from client import subscribeStatus
from publish import publish
from sym_key_generator import encrypt_public

# Load the packages
import datetime
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

end = time.time()
print("starting of the program till loading packages ", end-start)

start = time.time()
# load the files of list of sensors, units,types and key. All the files are in data folder
list_sensor = pd.read_csv("data/list_sensor1.csv",
                          delimiter=",", names=["id", "factor"])
list_units = pd.read_csv("data/list_units1.csv",
                         delimiter=",", names=["id", "factor"])
list_type = pd.read_csv("data/list_types1.csv",
                        delimiter=",", names=["id", "factor"])

# load the training dataset
df = pd.read_csv("data/training_data.csv")
total_row = df.shape[0]
trial_row = int(total_row-(total_row*0.25))
print("total rows ", total_row)

# the original combination of sensor, type and units
a = df.groupby(["Sensor", "Type", "Units"])[
               "Sensor"].unique().to_frame(name="1").reset_index()
original_combination = a.drop("1", 1)

# function to factor the columns of sensor,types and units
# Function1


def factorize(obj, obj_list, table, data, write_to_file):
	# print(data[obj].unique())
	if(write_to_file):
		data_s = pd.DataFrame(data[obj].unique())
		new_sensor = data_s[~data_s[0].isin(obj_list.id)]
		ns = []
		if(len(new_sensor) > 0):
			l = len(obj_list)
			for s in new_sensor[0]:
				n = [s, l]
				l = l+1
				ns.append(n)
			ns = pd.DataFrame(ns, columns=["id", "factor"])
			ns.to_csv(table, mode='a', header=False, index=False)

	obj_list = pd.read_csv(table, delimiter=",", names=["id", "factor"])
	l = len(obj_list)
	for i in range(0, l):
		if(len(data.loc[data[obj] == obj_list.id[i]]) > 0):
			data.loc[data[obj] == obj_list.id[i], obj] = obj_list.factor[i]
	# print(data[obj].unique())


# Function 2
'''
accepts two parameters.
    First is the dataframe of combinations of original dataset
    second is the test dataset
It then uses the group by to create the combinations
Both are merged using the inner. So it will have the common ones in original and test
Combine the new (c) with that of test (b).
use duplicates only to keep the differnces
'''


def spoof_detect(a, df1):
    b = df1.groupby(["Sensor", "Type", "Units"])[
                    "Sensor"].unique().to_frame(name="1").reset_index()
    b = b.drop("1", 1)
    c = (b.merge(a, how="inner"))
    fake = pd.concat([c, b], sort=False)
    # print(fake)
    # print(fake.drop_duplicates(keep=False))
    return fake.drop_duplicates(keep=False)


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
test = df.loc[trial_row+1:total_row, ]

# create the datasets to apply machine learning
x_train, y_train, x_test, y_test = train[x], train[y], test[x], test[y]

# Decision Tree algorithm
decision = DecisionTreeClassifier().fit(x_train, y_train)
decision_yhat = decision.predict(x_test)
print("training accuracy ", (decision.score(x_test, y_test))*100)
confusion_matrix(decision_yhat, y_test)

end = time.time()
print("After loading till the end of first training and testing ", end-start)

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
		if(temp_data.shape[0]>0):
			temp_data=temp_data.drop_duplicates()
			print("Number of rows for testing",temp_data.shape[0])
			# Checking  the existance of dummy or spoof data
			if(len(spoof_detect(original_combination,temp_data))==0):
				#call the function to factorise
				factorize('Sensor',list_sensor,'data/list_sensor1.csv',temp_data,False)
				factorize('Type',list_type,'data/list_types1.csv',temp_data,False)
				factorize('Units',list_units,'data/list_units1.csv',temp_data,False)

				temp_test= temp_data[x]
				decision_yhat = decision.predict(temp_test)

				flagged_false=(decision_yhat == 0).sum()
				flagged_true=(decision_yhat == 1).sum()

				test_acc=100-(flagged_true/flagged_false)
				print("amount of true readings are ",test_acc)
				end=time.time()
				print("Time taken for the analysis after receving the data ",end-start)
				if(test_acc>99.90):
					sym_key()
					benchmark(name_of_dc)
					clearFiles()
				else:
					# the function below publishes the decision back through publish
					publish("sensor_sym_key","abort")
					# publish(name_of_dc,"nodata")
					encrypt_public("nodata")
					benchmark(name_of_dc)
					clearFiles()
					abort_reason("accuracy_issues",str(test_acc))

			else:
				# the function below publishes the decision back through publish
				publish("sensor_sym_key","abort")
				encrypt_public("nodata")
				benchmark(name_of_dc)
				print("contain spoof datas and they are \n",spoof_detect(original_combination,temp_data))
				abort_reason("error"," \n")
				spoof_detect(original_combination,temp_data).to_csv("/home/pi/Documents/error.log",mode="a",index=False) # save the error details with time
				end=time.time()
				print("Time taken for the analysis after receving the data ",end-start)
				clearFiles()

		else:
			# publish(name_of_dc,"nodata")
			publish("sensor_sym_key","abort")
			encrypt_public("nodata")
			print("nodata")
			benchmark(name_of_dc)
			abort_reason("no_data","no data available in the sensors")
			clearFiles()
		
		mess=None

