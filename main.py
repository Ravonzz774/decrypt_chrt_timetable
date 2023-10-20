import requests
import base64
import codecs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from flask import Flask, jsonify


def get_token():
    url = "https://chrt.remmody.ru/v2/api/token"

    headers = {
        "BotKey": "ncoD7LJq-c7b3?Ka7G-aDfRsoMBNCgKKF-Pvu7oG/gMg2i1U9gqLBSAa!83w/?9PioybXfokFm=hSk1VMKlMx5BNx9PsLPYxnU5NiLEBRpYNkCu7pUZARxR5cfewgOD2"
    }
    response = requests.post(url, headers=headers)
    data = response.json()
    jwtToken = data.get("token")

    return jwtToken


def get_data_encrypted(token):
    url = "https://chrt.remmody.ru/v2/api"
    headers = {"Authorization": "Bearer " + token}

    response = requests.get(url, headers=headers)

    return response.text


# Обработка полученных данных
def decrypt_data(encrypted_data):
    try:
        key = base64.b64decode("NGM5NjVlOWUyMWVlYjNhNTZhZWQ3YTQzNjg3NTc1MWU=")
        iv = base64.b64decode("MjljNzZlYjU0MjA1MTg0YQ==")
        cipher_text = base64.b64decode(encrypted_data)

        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()

        decrypted_bytes = decryptor.update(cipher_text) + decryptor.finalize()

        padder = padding.PKCS7(128).unpadder()
        decrypted_text = padder.update(decrypted_bytes) + padder.finalize()

        return decrypted_text.decode("utf-8")
    except Exception as e:
        print("Ошибка при дешифровании данных:", e)
        raise e

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    token = get_token()
    encrypted_data = get_data_encrypted(token)
    data = decrypt_data(encrypted_data)
    return data

if __name__ == "__main__":
    app.run()
