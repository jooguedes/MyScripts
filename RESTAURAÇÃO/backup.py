from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from sh import openssl
import sys
import base64

if len(sys.argv) < 4:
    print("Ex: python backup.py [chave ssh] [arquivo.enc] [arquivo.txt]")

else:
    key = sys.argv[1]
    filename = sys.argv[2]
    password = sys.argv[3]

    chave = ""
    with open(password, "r") as f:
        chave = f.read()

    file = open(key)
    privatekey = file.read()
    file.close()

    rsakey = RSA.importKey(privatekey)
    rsakey = PKCS1_OAEP.new(rsakey)

    password = rsakey.decrypt(base64.b64decode(chave)).decode()

    print(password)

    p = openssl.enc("-d", "--aes-256-cbc", "-salt", "-pass", "pass:%s" % password, "-in", filename, "-out", "%s.sql.gz" % filename[:-4])

    print(p)
