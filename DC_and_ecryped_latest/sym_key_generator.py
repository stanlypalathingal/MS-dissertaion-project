from cryptography.fernet import Fernet
import asymcrypt
from publish import publish

def sym_key():
    sym_key=Fernet.generate_key()
    #print(sym_key)
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
    
def Decryption(encrypted_data):
    # print("data received here as ",type(encrypted_data))
    encrypted_data=encrypted_data.decode("utf-8")
    try:
		#print("inside")
        new_rnd_bytes = bytes.fromhex(encrypted_data)
        decrypted_data = asymcrypt.decrypt_data(new_rnd_bytes,"data/private_key.pem")
        print('Decrypted data is :', decrypted_data)
        with open('data/data_request.csv','w') as f:
            f.write("\n"+str(decrypted_data))
        f.close()
    except:
        print("not encrypted")
