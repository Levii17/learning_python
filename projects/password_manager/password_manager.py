# THIS IS NOT A SECURE WAY TO STORE PASSWORDS! THIS IS JUST A FUN PYTHON PROJECT FOR LEARNING PURPOSES.
import base64
import hashlib
import os
from cryptography.fernet import Fernet

# --- Key Generation / Loading Helper ---
def write_key():
    """Run this once if you don't have a 'key.key' file yet."""
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    # Automatically generate a key file if it doesn't exist so the script doesn't crash
    if not os.path.exists('key.key'):
        write_key()
        
    with open('key.key', 'rb') as file:
        key = file.read()
    return key

# --- Main Program Logic ---
master_pwd = input("What is the master password? ")

# 1. Load the base key
base_key = load_key()

# 2. Combine the base key and master password, then hash them to exactly 32 bytes
combined_data = base_key + master_pwd.encode()
hashed_key = hashlib.sha256(combined_data).digest()

# 3. Base64 encode the 32-byte hash to make it Fernet-compatible
fernet_key = base64.urlsafe_b64encode(hashed_key)
fer = Fernet(fernet_key)

def view():
    # Check if the file exists yet to prevent FileNotFoundError
    if not os.path.exists('passwords.txt'):
        print("No passwords saved yet!")
        return

    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            if not data or '|' not in data:
                continue
            
            user, passw = data.split('|')
            try:
                # Decrypting will fail if the master password is wrong
                decrypted_pwd = fer.decrypt(passw.encode()).decode()
                print('User:', user, '| Password:', decrypted_pwd)
            except Exception:
                print(f"User: {user} | Password: [Could not decrypt - Wrong Master Password?]")

def add():
    name = input('Account Name: ')
    pwd = input('Password: ')

    with open('passwords.txt', 'a') as f:
        # Encrypt the password and write it to the file
        encrypted_pwd = fer.encrypt(pwd.encode()).decode()
        f.write(name + '|' + encrypted_pwd + '\n')

while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()

    if mode == 'q':
        break
    elif mode == 'view':
        view()
    elif mode == 'add':
        add()
    else:
        print('Invalid mode.')
        continue