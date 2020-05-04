import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


df=pd.read_csv("Sample dataset values.txt")

df.loc[df['Sensor']=='sensor01','Sensor']=0
df.loc[df['Sensor']=='sensor02','Sensor']=1
df.loc[df['Sensor']=='sensor03','Sensor']=2

df.loc[df['Variable']=='PM10','Variable']=0
df.loc[df['Variable']=='PM 4','Variable']=1
df.loc[df['Variable']=='NO','Variable']=2
df.loc[df['Variable']=='PM2.5','Variable']=3
df.loc[df['Variable']=='PM1','Variable']=4
df.loc[df['Variable']=='Particle Count','Variable']=5
df.loc[df['Variable']=='O3','Variable']=6
df.loc[df['Variable']=='NO2','Variable']=7

df.loc[df['Name']=='PER_AIRMON_MESH1976150','Name']=0

df.loc[df['Units']=='ugm -3','Units']=0
df.loc[df['Units']=='Kgm -3','Units']=1
df.loc[df['Units']=='ppb','Units']=2

df.loc[df['Flagged as Suspect Reading']==False,'Flagged as Suspect Reading']=0
df.loc[df['Flagged as Suspect Reading']==True,'Flagged as Suspect Reading']=1

x=['Sensor', 'Name', 'Variable', 'Units','Value']
y=['Flagged as Suspect Reading']
train=df.loc[1:200,]
test=df.loc[201:267,]

x_train,y_train,x_test,y_test = train[x],train[y],test[x],test[y]

#confusion Matrix
def ConfusionMatrix(x,y):
    a = confusion_matrix(x,y)
    print(a)
    b = (a[0][0]+a[1][1])/(a[1][1]+a[0][1]+a[0][0]+a[1][0])
    return round(b*100,2)

#Decision Tree
decision = DecisionTreeClassifier(max_depth=5).fit(x_train, y_train)
decision_yhat = decision.predict(x_test)

print(decision.score(x_test,y_test))

decision_acc= ConfusionMatrix(decision_yhat,y_test)
print(decision_acc)

f1_score(decision_yhat,y_test) *100

print(precision_score(decision_yhat,y_test) *100)
print(recall_score(decision_yhat,y_test) *100)