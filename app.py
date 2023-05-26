from flask import Flask, render_template, request
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode_decode', methods=['POST'])
def encode_decode():
    key = request.form['private_key']
    message = request.form['message']
    mode = request.form['mode']

    if mode == 'e':
        result = Encode(key, message)
    elif mode == 'd':
        result = Decode(key, message)
    else:
        result = 'Invalid Mode'

    return render_template('result.html', result=result)

# function to encode
def Encode(key, message):
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        encoded_char = (ord(message[i]) + ord(key_c)) % 65536
        enc.append(chr(encoded_char))

    encoded_str = "".join(enc)
    encoded_bytes = encoded_str.encode("utf-8")
    encoded_base64 = base64.urlsafe_b64encode(encoded_bytes).decode("utf-8")
    return encoded_base64

# function to decode
def Decode(key, message):
    dec = []
    decoded_base64 = base64.urlsafe_b64decode(message).decode("utf-8")
    for i in range(len(decoded_base64)):
        key_c = key[i % len(key)]
        decoded_char = (65536 + ord(decoded_base64[i]) - ord(key_c)) % 65536
        dec.append(chr(decoded_char))

    return "".join(dec)

# handle surrogate pairs in encoding
def Encode(key, message):
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        encoded_char = (ord(message[i]) + ord(key_c)) % 65536
        if encoded_char >= 0xD800 and encoded_char <= 0xDBFF:
            enc.append(message[i])
        else:
            enc.append(chr(encoded_char))

    encoded_str = "".join(enc)
    encoded_bytes = encoded_str.encode("utf-8")
    encoded_base64 = base64.urlsafe_b64encode(encoded_bytes).decode("utf-8")
    return encoded_base64

# handle surrogate pairs in decoding
def Decode(key, message):
    dec = []
    decoded_base64 = base64.urlsafe_b64decode(message).decode("utf-8")
    i = 0
    while i < len(decoded_base64):
        key_c = key[i % len(key)]
        decoded_char = (65536 + ord(decoded_base64[i]) - ord(key_c)) % 65536
        if decoded_char >= 0xD800 and decoded_char <= 0xDBFF:
            dec.append(decoded_base64[i:i+2])
            i += 2
        else:
            dec.append(chr(decoded_char))
            i += 1

    return "".join(dec)

if __name__ == '__main__':
    app.run(debug=True)
