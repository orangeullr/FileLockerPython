#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, send_file, request
import logging
from io import BytesIO
from zipfile import ZipFile
from controller.fileLockController import fileLockController

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

# context = ssl.SSLContext()
# context.load_cert_chain('cert.crt', keyfile='key.key', password='')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def home():
    return render_template('pages/landing.html')

@app.route('/encrypt', methods=['GET'])
def encrypt():
    return render_template('pages/encryptor.html')

@app.route('/decrypt', methods=['GET'])
def decrypt():
    return render_template('pages/decryptor.html')

@app.route('/encryptor', methods=['POST'])
def encryptor():
    if request.method == 'POST':
        # Read the entire request body as bytes
        file_bytes = request.files['file'].read()
        file_name = request.files['file'].filename
        controller = fileLockController()
        output_buffer, key = controller.encrypt_file(file_bytes)
        memory_file = BytesIO()
        
        with ZipFile(memory_file, 'w') as zf:
            zf.writestr(f"{file_name}.key", key)
            zf.writestr(f"{file_name}.lock", output_buffer)

        memory_file.seek(0)
        filenamelockfile=f"encrypted_{file_name}.zip"
        return send_file(memory_file, as_attachment=True, download_name=filenamelockfile)
    return "Please send a POST request with file data."


@app.route('/decryptor', methods=['POST'])
def decryptor():
    if request.method == 'POST':
        # Read the entire request body as bytes
        file_bytes = request.files['lockfile'].read()
        file_name = request.files['lockfile'].filename
        key_bytes = request.files['keyfile'].read()
        controller = fileLockController()
        output_buffer = controller.decrypt_file(key_bytes, file_bytes)
        memory_file = BytesIO()
        memory_file.write(output_buffer)
        memory_file.seek(0)
        unlockfilename=f"decrypted_{file_name.replace('.lock', '')}"
        return send_file(memory_file, as_attachment=True, download_name=unlockfilename)
    return "Please send a POST request with file data."

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#--------------------------#
# Launch defined in run.py #
#--------------------------#

if __name__ == '__main__':
    app.run(debug=True, port=8000)
