"""
authentication.md:

Summary
This module is used to verify user tokens and record user's behavior, including:
request URL, parameters, frequency, etc.
"""

import os

import rsa

print("Loading RSA Key ... ")
try:
    PUBLIC_KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public_key.pem')
    PRIVATE_KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'private_key.pem')
    with open(PUBLIC_KEY_PATH, 'r') as f:
        PUBLIC_KEY_CONTENT = f.read()
        PUBLIC_KEY = rsa.PublicKey.load_pkcs1(PUBLIC_KEY_CONTENT.encode())
    with open(PRIVATE_KEY_PATH, 'r') as f:
        PRIVATE_KEY = rsa.PrivateKey.load_pkcs1(f.read().encode())
    print("RSA Key Loaded.")
except FileNotFoundError:
    print("[ERROR] Can not find private_key.pem or public_key.pem")
    exit(-1)


def decrypt(message):
    return rsa.decrypt(message, PRIVATE_KEY).decode()
