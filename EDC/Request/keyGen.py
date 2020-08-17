from Crypto import Random
from Crypto.PublicKey import RSA
import asymcrypt


def keyGen():
    keyLngth = 256 * 8;  # Give key length of 2048
    pvtKey = RSA.generate(keyLngth, Random.new().read)
    pubKey = pvtKey.publickey()
    # Write the public key to pub.txt
    pubFl = open("pub2.pem", "wb")
    pubFl.write(pubKey.export_key())
    pubFl.close()

    # Write private key to priv.txt
    pvtFl = open("priv2.pem", "wb")
    pvtFl.write(pvtKey.export_key())
    pvtFl.close()


if __name__ == "__main__":
    keyGen()
    print("Key Generated")
