from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
import pandas as pd
from publish import publish

def sym_key():
    sym_key=Fernet.generate_key()
    print(sym_key)
    publish("sensor_sym_key",sym_key)
    # df1=pd.read_csv("data/pub_Key_store.csv",names=["public"])
    # a=df1.public[0]
    # print(df1)
    new_key=open('data/pub_Key_store.csv').readlines()
    new_key = ''.join(new_key)
    publish("sensor_sym_key",new_key)
    



