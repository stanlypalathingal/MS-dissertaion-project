from cryptography.fernet import Fernet
# from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization # for creating pem
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pandas as pd
from publish import publish
import ast

def sym_key():
    sym_key=Fernet.generate_key()
    print(sym_key)
    publish("sensor_sym_key",sym_key)
    encrypt_public(sym_key)
    
def encrypt_public(key):
    # open the .pem file
    new_key=open('data/temporary_store.csv').readlines()
    new_key = ''.join(new_key)
    print(new_key)
    print("data/"+new_key+".pem")
    with open("data/ThisIsMyPublicKey.pem","rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    encrypt = public_key.encrypt(key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )
    publish("DC_1_message",encrypt)
    # print(encrypt)
    # decrypt_message(encrypt)

def decrypt_message(message):
    with open("data/private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    original_message = private_key.decrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
     )
    )
    print(original_message)

