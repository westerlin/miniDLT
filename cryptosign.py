# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 12:13:55 2018

@author: raw
"""

import os
import ecdsa
import codecs

decode_hex = codecs.getdecoder("hex_codec")
encode_hex = codecs.getencoder("hex_codec")

class CryptographicSignature:
    
    def __init__(self,privatekey=None):
        self.private = privatekey
        if (privatekey):
            self.signing = ecdsa.SigningKey.from_string(privatekey, curve=ecdsa.SECP256k1)
            self.public = self.signing.get_verifying_key()
        else:
            self.signing = None
            self.public = None
    
    def generate(self):
        rawkey = os.urandom(32)
        self.private = rawkey
        self.signing = ecdsa.SigningKey.from_string(rawkey, curve=ecdsa.SECP256k1)
        self.public = self.signing.get_verifying_key()
        
    def getPublicKey(self):
        return encode_hex(self.public.to_string())[0]
        
    def signMessage(self,message,secretKey=None):
        if (secretKey):
            externalSigningKey = ecdsa.SigningKey.from_string(decode_hex(secretKey)[0],curve=ecdsa.SECP256k1)
            signature = externalSigningKey.sign(message.encode('utf-8'))
        else:
            signature = self.signing.sign(message.encode('utf-8'))
        return str(encode_hex(signature)[0],'utf-8'),signature
    
    def verifyMessage(self,message,signature):
        try:
            assert self.public.verify(decode_hex(signature)[0],message.encode('utf-8'))
            return True
        except ecdsa.keys.BadSignatureError:
            return False
