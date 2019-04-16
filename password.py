from cryptography.fernet import Fernet

def encrypt(password):
    # key = Fernet.generate_key() #this is your "password"
    # cipher_suite = Fernet(key)
    # encoded_text = cipher_suite.encrypt(bytes(password, "utf-8"))
    output = []
    output.append(str(password))
    output.append(str('x'))
    return output

def decrypt(password, key):
    # key = bytes(key, "utf-8")
    # cipher_suite = Fernet(key)
    # password = bytes(password, "utf-8")
    # decoded_text = cipher_suite.decrypt(password)
    return (str(password))

# x=encrypt("123456")

# y=decrypt(x[0],x[1])
# print(x)
# print(y)