from cryptography.fernet import Fernet
import asymcrypt
from publish import publish

def sym_key():
    sym_key=Fernet.generate_key()
    print(sym_key)
    publish("result",sym_key)
    encrypt_public(sym_key)
    
def encrypt_public(key):
    #open the file conatining the topic
    new_key=open('data/temporary_store.txt').read().replace('\n','')
    # print(new_key)
    # print("data/"+new_key+".pem")
    encrypted_data = asymcrypt.encrypt_data(key,"data/"+new_key+".pem")
    hex_str = encrypted_data.hex()
    # print(hex_str)
    publish(new_key,hex_str)