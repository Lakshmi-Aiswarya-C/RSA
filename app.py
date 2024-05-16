import os
import uuid 
import random
import math
from flask import Flask, render_template, request, send_file,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('IS.html')


def generate_random_e(phi_n):
    e=7
    return e
        
def mod_inverse(a, m):
    b = 0
    if a < m:
        b = a
        a = m
    else:
        b = m

    t1 = 0
    t2 = 1
    t = 0

    while b != 0:
        q = a // b
        r = a % b
        a = b
        b = r
        t = t1 - q * t2
        t1 = t2
        t2 = t

    if t1 < 0:
        t1 += m

    return t1

@app.route('/download_public_key')
def download_public_key():
    # Generate the public key text file
    p = request.args.get('p')
    q = request.args.get('q')
    p=int(p)
    q=int(q)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = generate_random_e(phi_n)
    publicKey = f"{e},{n}"

    with open('publickey.txt', 'w') as public_key_file:
        public_key_file.write(str(publicKey))

    return send_file('publickey.txt', as_attachment=True, download_name='publickey.txt')

@app.route('/download_private_key')
def download_private_key():
    # Generate the private key text file
    p = request.args.get('p')
    q = request.args.get('q')
    p=int(p)
    q=int(q)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = generate_random_e(phi_n)
    d = mod_inverse(e, phi_n)
    privateKey = f"{d},{n}"

    with open('privatekey.txt', 'w') as private_key_file:
        private_key_file.write(str(privateKey))

    return send_file('privatekey.txt', as_attachment=True, download_name='privatekey.txt')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']

        if not uploaded_file:
            return jsonify({"success": False, "message": "No file uploaded."})

        upload_directory = 'uploads'

        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)

        unique_filename = str(uuid.uuid4()) + '.txt'
        file_path = os.path.join(upload_directory, unique_filename)

        uploaded_file.save(file_path)

        # You can add additional processing here if needed

        upload_status = "File uploaded successfully."

        return jsonify({"success": True, "message": upload_status})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})



if __name__ == "__main__":
    app.run()