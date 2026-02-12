# FileLockerPython

A simple command-line utility and web service port for encrypting and decrypting individual files using **AES-256 CBC mode**.

This tool is designed for secure file protection using industry-standard symmetric encryption.

---

## Features

* AES-256 CBC 
* Secure random IV generation
* Encrypt single files
* Decrypts single files
* Cross-platform compatible with python runtime

---

## Requirements

* Python 3.9+ (or specify your runtime)
* Required dependencies listed in `requirements.txt` for both the "standalone" and "web service" versions

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Standalone

```bash
python filelock.py [-h] {encrypt,decrypt} input_file output_file
```
encrypt requires input and output file names to be declared. Output file is the new encrypted file. Input file is the file to be encrypted and is not removed.
A file called "encryption.key" will be created.
Decrypt operation requires that "encryption.key" file to be present in the root directory.

### Web Service
It comes docker ready.
The UI should be pretty simple to navigate and quite intuitive.

You can build this docker file and host it on your local system if you'd like. If not, it's under a GPL license so have at it and modify it as you'd like.

```bash
cd webservice/
docker build -f Dockerfile -t filelockerpython
docker run -p 8000:8000 filelockerpython
```

---

## How It Works

1. A secure random Initialization Vector (IV) is generated of len 16 bytes.
2. The file is encrypted using AES-256-CBC.
3. The IV is prepended to the encrypted output file.
4. The key created is written to a file. This file is not password protected.
5. During decryption, both the key and lock file are required in order to produce the locked file's original state.


---

## Security Notes

* Use at your own risk. This author will assume no responsibility for your implementation.
* Never reuse encryption keys across sensitive systems.
* Keep encrypted files and key files stored separately.
* For high-security uses, please use in conjunction with FIPS compliant systems to at-rest encryption (Level 2 or 3)
