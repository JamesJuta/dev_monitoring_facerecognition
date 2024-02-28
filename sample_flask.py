# from flask import Flask, session, request, render_template
# from flask_session import Session

# app = Flask(__name__)

# # Configure session to use filesystem (you can change this to use other session backends)
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
# Session(app)

# @app.route('/')
# def index():

#     # Retrieve username and password from query parameters
#     username = request.args.get('username')
#     password = request.args.get('password')

#     # Retrieve username and password from session
#     # username = session.get('username')
#     # password = session.get('password')

#     # Here you can use the username and password to display user information or perform other actions
#     return render_template("sample.html", username=username)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, render_template
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad
# import base64

# app = Flask(__name__)

# # Decryption function
# def decrypt_data(encrypted_data, key, iv):
#     # Ensure the key is the correct length
#     key = key[:32]  # Trim to 32 bytes if longer

#     # Convert IV from hexadecimal string to bytes
#     iv_bytes = bytes.fromhex(iv)

#     cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
#     decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))

#     # Unpad the decrypted data
#     decrypted_data = unpad(decrypted_data, AES.block_size)

#     return decrypted_data.decode('utf-8').strip()  # Remove leading/trailing whitespace

# @app.route('/')
# def index():
#     # Retrieve encrypted data and IV from the query parameters
#     encrypted_data = request.args.get('data')
#     hex_iv = request.args.get('iv')

#     if encrypted_data and hex_iv:
#         # Decrypt the data using the same key used in PHP
#         decryptionKey = b'g5K8Ht+6oCOOG8IJnZIoR59Doa8shfBjqRvvhb9yIGU='
#         try:
#             decrypted_username = decrypt_data(encrypted_data, decryptionKey, hex_iv)
#             return render_template('sample.html', username=decrypted_username)
#         except Exception as e:
#             return f"Error decrypting data: {str(e)}"
#     else:
#         return "No data to decrypt"

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, session
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

app = Flask(__name__)
app.secret_key = b'secret_key'  # Set a secret key for session management

# Decryption function
def decrypt_data(encrypted_data, key, iv):
    # Ensure the key is the correct length
    key = key[:32]  # Trim to 32 bytes if longer

    # Convert IV from hexadecimal string to bytes
    iv_bytes = bytes.fromhex(iv)

    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))

    # Unpad the decrypted data
    decrypted_data = unpad(decrypted_data, AES.block_size)

    return decrypted_data.decode('utf-8').strip()  # Remove leading/trailing whitespace

@app.route('/')
def index():
    # Retrieve encrypted data and IV from the query parameters
    encrypted_data = request.args.get('data')
    hex_iv = request.args.get('iv')

    if encrypted_data and hex_iv:
        # Decrypt the data using the same key used in PHP
        decryptionKey = b'g5K8Ht+6oCOOG8IJnZIoR59Doa8shfBjqRvvhb9yIGU='
        try:
            decrypted_username = decrypt_data(encrypted_data, decryptionKey, hex_iv)
            session['username'] = decrypted_username  # Store decrypted username in session
            return render_template('sample.html', username=decrypted_username)
        except Exception as e:
            return f"Error decrypting data: {str(e)}"
    else:
        return "No data to decrypt"

# Example route to demonstrate accessing session variable in another route
@app.route('/profile')
def profile():
    # Access the decrypted username stored in session
    decrypted_username = session.get('username')
    if decrypted_username:
        return f"Welcome to your profile, {decrypted_username}!"
    else:
        return "You are not logged in."

if __name__ == '__main__':
    app.run(debug=True)
