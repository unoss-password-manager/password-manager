import shelve
import yaml
import os, random, string
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode, urlsafe_b64encode

def loadConfig():
    stream = open('./config/config.yml', 'r')
    config = yaml.load(stream, Loader=yaml.SafeLoader)
    stream.close()
    return config

def openData(fileName):
    config = loadConfig()
    file = shelve.open(config["path"]["data"] + fileName)
    return file

def generateKey():
    print('Generating Key...')
    key = Fernet.generate_key()
    return key

def getFernetKey():
    #Read Key from keyfile
    config = loadConfig()
    filename = config["path"]["key"]
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    if os.path.exists(filename):
        #open file and get key
        keyFile = open(filename)
        keyTemp = keyFile.read()
        key = keyTemp.encode()
    else:
        #generate and save key if it doesn't exist
        keyFile = open(filename, 'w')
        key = generateKey()
        keyFile.write(key.decode())

    fernetKey = Fernet(key)
    keyFile.close()
    return fernetKey

def getFernetSuite(keyword, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    key = urlsafe_b64encode(kdf.derive(keyword.encode()))        
    return Fernet(key)

def decrypt(encryptedText, keyword, doubleSecure=False):
    ciphertext = b64decode(encryptedText)
    salt = ciphertext[:16]
    ciphertext = ciphertext[16:]
    fernet_suite = getFernetSuite(keyword, salt)
    unciphered_text = fernet_suite.decrypt(ciphertext)

    if doubleSecure:
        fernet_key = getFernetKey()
        unciphered_text = fernet_key.decrypt(unciphered_text)

    return unciphered_text.decode()

def encrypt(strToEncrypt, keyword, doubleSecure=False):
    chars=string.ascii_uppercase + string.digits
    size = 16
    salt = ''.join(random.choice(chars) for x in range(size))
    salt = salt.encode()
    fernet_suite = getFernetSuite(keyword, salt)
    
    if doubleSecure:
        fernet_key = getFernetKey()
        strToEncrypt = fernet_key.encrypt(strToEncrypt.encode())
    else:
        strToEncrypt = strToEncrypt.encode()
        
    ciphered_text = fernet_suite.encrypt(strToEncrypt)
    return b64encode(salt + ciphered_text)    
