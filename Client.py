# Client 1 code
import requests
from Crypto.Cipher import AES
from base64 import b64encode

# Secret key for encryption (must be the same on all clients and server)
secret_key = b'This_is_my_Distributed_Computing'  # 16 bytes for AES-128

# AES cipher initialization
cipher = AES.new(secret_key, AES.MODE_EAX)

def login(username, password):
    # Authenticate the user (simplified for demonstration)
    # You would replace this with your actual authentication logic
    if username == 'user1' and password == 'password1':
        return True
    else:
        return False

def encrypt_secret_part(secret_part):
    # Encrypt the secret part
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ciphertext, tag = cipher.encrypt_and_digest(secret_part.encode('utf-8'))
    encrypted_secret_part = ':'.join([nonce, b64encode(tag).decode('utf-8'), b64encode(ciphertext).decode('utf-8')])
    return encrypted_secret_part

def submit_secret_part(secret_part):
    # Encrypt the secret part
    encrypted_secret_part = encrypt_secret_part(secret_part)
    
    # Send the encrypted secret part to the server
    payload = {'client_id': 0, 'secret_part': encrypted_secret_part}
    response = requests.post('http://localhost:5000/submit_secret', data=payload)
    print(response.text)

if __name__ == '__main__':
    # Example usage
    if login('user1', 'password1'):
        submit_secret_part('p1')
    else:
        print("Invalid credentials.")
