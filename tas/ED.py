import base64
import pyDes
from Crypto.Cipher import DES3
def encrypt_3des(clear_text):
    key="vinoth-key"
    clear_text_byte = clear_text.encode('utf-8')
    key_byte = key.encode('utf-8')
    key_byte = key_byte.ljust(24, "\0".encode('utf-8'))
    if len(key_byte) > 24:
        key_byte = key_byte[:24]

    k = pyDes.triple_des(key_byte, pyDes.ECB, IV = None, pad = None, padmode = pyDes.PAD_PKCS5)
    d = k.encrypt(clear_text_byte)

    return base64.b64encode(d).decode('utf-8')
def decrypt_3des(data):
    key="vinoth-key"
    data_byte = base64.b64decode(data.encode('utf-8'))
    key_byte = key.encode('utf-8')
    key_byte = key_byte.ljust(24, "\0".encode('utf-8'))
    if len(key_byte) > 24:
        key_byte = key_byte[:24]

    cryptor = DES3.new(key_byte, DES3.MODE_ECB)
    c_text = cryptor.decrypt(data_byte)

    # PKCS#5
    pad_len = ord(c_text.decode('utf-8')[-1])
    clear_text = c_text.decode('utf-8')[:-pad_len]

    return clear_text

def decrypt_all(data):
	
	for key ,value in data.items():
		for subkey,subvalue in value.items():
			data[key][subkey]=decrypt_3des(subvalue)
	return data

