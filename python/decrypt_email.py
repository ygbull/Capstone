from Crypto.Cipher import AES
from ast import literal_eval

ciphertext = ""

with open("keylog.txt", "r") as f:
    ciphertext = f.read()

aes = AES.new(b"capstonepassword", AES.MODE_CFB, iv=b"564initialvector")
text = aes.decrypt(literal_eval(ciphertext))

with open("keylog.txt", "w") as f:
    f.write(text.decode("utf-8"))
