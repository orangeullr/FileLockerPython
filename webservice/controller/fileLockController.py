import os
import sys
from io import BytesIO
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class fileLockController:
    def __init__(self):
        pass
        
    def generate_aes_key(self):
        # Generate a 256-bit (32-byte) AES key
        # You can modify the number of bytes by changing parameter of unsigned random
        key = os.urandom(32)
        return key

    def encrypt_file(self, input):
        # Pad the plaintext to be a multiple of the block size
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(input) + padder.finalize()

        # Generate a random 16-byte IV
        iv = os.urandom(16)
        key = self.generate_aes_key()
        # Create a Cipher object
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypt the padded data
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Write the IV and ciphertext to the output file buffer
        return  iv + ciphertext, key


    def decrypt_file(self, key, input):
        # Read the encrypted file
        memory_file = BytesIO(input)
        iv = memory_file.read(16)  # The first 16 bytes are the IV
        ciphertext = memory_file.read()
    
        # Create a Cipher object
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()

        return plaintext
