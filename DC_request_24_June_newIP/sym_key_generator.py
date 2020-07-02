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
    name_of_dc=open('data/temporary_store.txt').read().replace('\n','')
    # print(name_of_dc)
    # print("data/"+name_of_dc+".pem")
    encrypted_data = asymcrypt.encrypt_data(key,"data/"+name_of_dc+".pem")
    hex_str = encrypted_data.hex()
    # print(hex_str)
    publish(name_of_dc,hex_str)
