from cryptography.fernet import Fernet
import asymcrypt
from publish import publish

def sym_key():
    sym_key=Fernet.generate_key()
    print(sym_key)
    publish("sensor_sym_key",sym_key)
    encrypt_public(sym_key)
    
def encrypt_public(key):
    #open the file conatining the topic
    new_key=open('data/temporary_store.txt').read().replace('\n','')
    # print(new_key)
    print("data/"+new_key+".pem")
    encrypted_data = asymcrypt.encrypt_data(key,"data/"+new_key+".pem")
    hex_str = encrypted_data.hex()
    # print(hex_str)
    publish(new_key,hex_str)
    
def Decryption(encrypted_data):
    print("data received here as ",type(encrypted_data))
    encrypted_data=encrypted_data.decode()
    print("converted the data as ",type(encrypted_data))

    new_rnd_bytes = bytes.fromhex(encrypted_data)
    decrypted_data = asymcrypt.decrypt_data(new_rnd_bytes,"dc2.pem")
    print('Decrypted data is :', decrypted_data)
