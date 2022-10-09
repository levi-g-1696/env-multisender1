def getEncryptStr(srcString,psw):
    from cryptography.fernet import Fernet

    key = Fernet.generate_key()  # store in a secure location
    # PRINTING FOR DEMO PURPOSES ONLY, don't do this in production code
    print("Key:", key.decode())
#getEncryptStr("","")
from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

key = Fernet.generate_key()
message = "tstPSW"
encr= encrypt(message.encode(),key)
decr= decrypt(encr, key).decode()
print (message , encr, decr)
import base64


