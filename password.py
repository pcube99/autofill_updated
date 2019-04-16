from cryptography.fernet import Fernet

def encrypt(password):
    key = Fernet.generate_key() #this is your "password"
    cipher_suite = Fernet(key)
    encoded_text = cipher_suite.encrypt(bytes(password, "utf-8"))
    output = []
    output.append(str(encoded_text).split("'")[1])
    output.append(str(key).split("'")[1])
    return output

def decrypt(password, key):
    key = bytes(key, "utf-8")
    cipher_suite = Fernet(key)
    password = bytes(password, "utf-8")
    decoded_text = cipher_suite.decrypt(password)
    return (str(decoded_text).split("'")[1])

#x=encrypt("milan")
#y=decrypt(x[0],x[1])
#print(x)
#print(y)