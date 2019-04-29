import rsa
import os

print("Load Private Key")

private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'private_key.pem')

with open(private_key_path, 'r') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read().encode())
