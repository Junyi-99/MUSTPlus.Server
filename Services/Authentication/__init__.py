"""
Authentication:

Summary
This module is used to verify user tokens and record user's behavior, including:
request URL, parameters, frequency, etc.
"""

import rsa
import os

print("Loading RSA Key ... ")
try:
    public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'public_key.pem')
    private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'private_key.pem')
    with open(public_key_path, 'r') as f:
        public_key_content = f.read()
        public_key = rsa.PublicKey.load_pkcs1(public_key_content.encode())
    with open(private_key_path, 'r') as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read().encode())
    print("RSA Key Loaded.")
except FileNotFoundError as e:
    print("[ERROR] Can not find private_key.pem or public_key.pem")
    exit(-1)


def decrypt(message):
    return rsa.decrypt(message, private_key).decode()
