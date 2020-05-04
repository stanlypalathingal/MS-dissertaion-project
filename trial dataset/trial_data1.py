#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().run_line_magic('autosave', '20')
import pandas as pd


# ### Load the data set
# The file is in '*.txt', but the format of the data inside the file is in 'csv'. So load the data directly as 'csv' 

# In[2]:


df=pd.read_csv("Sample dataset values.txt")


# In[3]:


df


# See  that the first coulmn is the serial number and will not add anything to the analysis

# In[4]:


df.columns[1:8,]


# ### Description of the objects and  not of the numerics

# In[5]:


df.describe(include='O')


# ### Unique elements of the columns
# The dataset has 8 columns and 267 records. Among these 'Sr No' , 'Timestamp' and 'Value' are numerics. Two of these fields are unique. 'Sr No' and 'Timestamp' are unique to each record. The column 'Values' are different for different sensors. The other columns there are repetitons.

# In[6]:


def uni(col):
    print("There are ",len(df[col].unique())," unique elements  of column ", col," and they are ", df[col].unique())


# In[7]:


list(map(uni,df[['Sensor', 'Name', 'Variable', 'Units','Flagged as Suspect Reading']]))


# In[ ]:




