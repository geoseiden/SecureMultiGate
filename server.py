# Server code
from flask import Flask, request, render_template
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

app = Flask(__name__)

# Secret key for encryption (must be the same on all clients and server)
secret_key = b'This_is_my_Distributed_Computing'  # 16 bytes for AES-128

# AES cipher initialization
cipher = AES.new(secret_key, AES.MODE_EAX)

# Secret phrase parts from each client (encrypted)
secret_parts_encrypted = [None, None, None]

flag = False

@app.route('/')
def main():
    if flag:
        return render_template('unlocked.html', content="Server Unlocked")  # Corrected render_template call
    else:
        return render_template('unlocked.html', content="Server Locked")
# Route to receive secret phrase parts from clients
@app.route('/submit_secret', methods=['POST'])
def submit_secret():
    global flag  # Add this line to indicate that we are modifying the global flag variable
    client_id = int(request.form['client_id'])
    secret_part_encrypted = request.form['secret_part']
    nonce, tag, ciphertext = secret_part_encrypted.split(":")
    nonce = b64decode(nonce)  # Decode nonce from base64 to bytes
    tag = b64decode(tag)
    ciphertext = b64decode(ciphertext)
    
    # Decrypt the secret part
    cipher = AES.new(secret_key, AES.MODE_EAX, nonce=nonce)
    secret_part = cipher.decrypt_and_verify(ciphertext, tag)
    
    secret_parts_encrypted[client_id] = secret_part
    
    # Check if all secret parts are received
    if all(secret_parts_encrypted):
        # Combine secret parts to form the complete phrase
        complete_phrase = b''.join(secret_parts_encrypted).decode('utf-8')
        
        # Check if the combined phrase unlocks the server
        if complete_phrase == 'p1p2p3':
            flag = True
            return "unlocked"
        else:
            return "Incorrect secret phrase. Access denied."
    else:
        return "Secret part received. Waiting for others..."

if __name__ == '__main__':
    app.run(debug=True)
