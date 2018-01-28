import os
import hashlib
import base58
import binascii
import ecdsa
import codecs

decode_hex = codecs.getdecoder("hex_codec")
encode_hex = codecs.getencoder("hex_codec")

rawkey = os.urandom(32)
#rawkey = b"363687ac41b83eeaf6f8eb5fde3a2ba98cfeaf01ddc5cd4df10e915b3ff64ea2"
#rawkey = decode_hex(b"363687ac41b83eeaf6f8eb5fde3a2ba98cfeaf01ddc5cd4df10e915b3ff64ea2")[0]

print("RAW:",rawkey)
hexcode = encode_hex(rawkey)
print("HEX;",hexcode)
decodedkey = decode_hex(hexcode[0])
print("DECODE",decodedkey)

#sk = ecdsa.SigningKey.from_string(decodedkey[0], curve=ecdsa.SECP256k1)
#SK is the private key for signing
sk = ecdsa.SigningKey.from_string(rawkey, curve=ecdsa.SECP256k1)
print("SK Private/Signing key \n  ",encode_hex(sk.to_string())[0])
#VK is the public key for verifying
vk = sk.get_verifying_key()
print("VK Public/Verification Key \n  ",encode_hex(vk.to_string())[0])

msg = b"Hello world"
msg1 = b"Hello world"

#Node sends the signature of the message and send
signature = sk.sign(msg)
print("Signature:",encode_hex(signature))

msg = b"hello world"
try:
    assert vk.verify(signature,msg)
    print("Signing was ok")
except ecdsa.keys.BadSignatureError:
    print("Signing was not ok")



#===============
"""
Example where public key is changed from object to string so it can be send over Network
"""
def example_sign_verify_msg():
    # Creates a "super" random key via OS
    private_key = encode_hex(os.urandom(32))[0]
    # Converts to a string
    private_key_str = str(private_key,'utf-8')
    print("My private key: " + private_key_str)
    # creates a signig key based on my private key
    sk = ecdsa.SigningKey.from_string(decode_hex(private_key)[0],curve=ecdsa.SECP256k1)
    print()
    # Verifying key is the same as public key
    public_key = sk.verifying_key
    #Converts to string
    public_key_str = str(encode_hex(public_key.to_string())[0],'utf-8')
    print("My public key: " + public_key_str)
    print()
    # Creates some message which can be signed
    msg = "My message"
    # Signs with signing key SK object - based on private key - signing key should be kept secret
    signed_msg = sk.sign(msg.encode('utf-8'))
    # Creates verifying key (public key) object from string
    vk = ecdsa.VerifyingKey.from_string(decode_hex(public_key_str)[0],curve=ecdsa.SECP256k1)
    print(msg)
    print(str(encode_hex(signed_msg)[0],'utf-8'))
    # Verifies signed message  based on verifikation key object
    vk.verify(signed_msg,msg.encode('utf-8'))
#================
