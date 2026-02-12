import os
import sys
import argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def generate_aes_key():
    # Generate a 256-bit (32-byte) AES key
    key = os.urandom(32)
    key_file = 'encryption.key'
    with open(key_file, 'wb') as f:
        f.write(key)
    print(f"Generated AES-256 Key and saved to {key_file}")
    return key

def encrypt_file(key, input_file_path, output_file_path):
    # Read the plaintext file
    with open(input_file_path, 'rb') as f:
        plaintext = f.read()

    # Pad the plaintext to be a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Write the IV and ciphertext to the output file
    with open(output_file_path, 'wb') as f:
        f.write(iv + ciphertext)

def decrypt_file(key, input_file_path, output_file_path):
    # Read the encrypted file
    with open(input_file_path, 'rb') as f:
        iv = f.read(16)  # The first 16 bytes are the IV
        ciphertext = f.read()

    # Create a Cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    # Write the plaintext to the output file
    with open(output_file_path, 'wb') as f:
        f.write(plaintext)

def main():
    parser = argparse.ArgumentParser(description='AES-256 Encryption/Decryption Tool')
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode: encrypt or decrypt')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')

    args = parser.parse_args()

    if args.mode == 'encrypt':
        key = generate_aes_key()
        encrypt_file(key, args.input_file, args.output_file)
    elif args.mode == 'decrypt':
        key_file = 'encryption.key'
        if not os.path.exists(key_file):
            print(f"Error: Key file '{key_file}' not found in the current directory.")
            sys.exit(1)
        with open(key_file, 'rb') as f:
            key = f.read()
        decrypt_file(key, args.input_file, args.output_file)

if __name__ == '__main__':
    main()
