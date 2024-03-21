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
#     # password = request.args.get('password')
#     token = request.args.get('token')


#     # Retrieve username and password from session
#     # username = session.get('username')
#     # password = session.get('password')

#     # Here you can use the username and password to display user information or perform other actions
#     return render_template("sample.html", username=username, token=token)

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


# from flask import Flask, request, render_template, session, redirect
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad
# import base64

# app = Flask(__name__)
# app.secret_key = b'secret_key'  # Set a secret key for session management

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
# def home():
#     # Retrieve encrypted data and IV from the query parameters
#     encrypted_data = request.args.get('data')
#     hex_iv = request.args.get('iv')

#     if encrypted_data and hex_iv:
#         # Decrypt the data using the same key used in PHP
#         decryptionKey = b'g5K8Ht+6oCOOG8IJnZIoR59Doa8shfBjqRvvhb9yIGU='
#         try:
#             decrypted_username = decrypt_data(encrypted_data, decryptionKey, hex_iv)
#             session['username'] = decrypted_username  # Store decrypted username in session
#             return render_template('sample.html', username=decrypted_username)
#         except Exception as e:
#             return f"Error decrypting data: {str(e)}"
#     else:
#         return "No data to decrypt"

# # Example route to demonstrate accessing session variable in another route
# # @app.route('/profile')
# # def profile():
# #     # Access the decrypted username stored in session
# #     decrypted_username = session.get('username')
# #     if decrypted_username:
# #         return f"Welcome to your profile, {decrypted_username}!"
# #     else:
# #         return "You are not logged in."
    
# # logout route 
# @app.route('/logout', methods=['POST'])
# def logout():
#     # Clear all session variables
#     session.clear()

#     # Redirect the user to the specified URL
#     return redirect("http://localhost/dev_monitoring_facerecognition/index.php")


# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask, request, session, jsonify, render_template
# from Crypto.Cipher import AES
# import base64
# import json
# import binascii

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# def my_decrypt(data, passphrase):
#     """
#     Decrypt using AES-256-CBC with iv
#     'passphrase' must be in hex, generate with 'openssl rand -hex 32'
#     """
#     try:
#         unpad = lambda s: s[:-s[-1]]
#         key = binascii.unhexlify(passphrase)
#         encrypted = json.loads(base64.b64decode(data).decode('ascii'))
#         encrypted_data = base64.b64decode(encrypted['data'])
#         iv = base64.b64decode(encrypted['iv'])
#         cipher = AES.new(key, AES.MODE_CBC, iv)
#         decrypted = cipher.decrypt(encrypted_data)
#         clean = unpad(decrypted).decode('ascii').rstrip()
#     except Exception as e:
#         print("Cannot decrypt datas...")
#         print(e)
#         exit(1)
#     return clean

# @app.route('/')
# def home():
#     if 'attempt_count' not in session:
#         session['attempt_count'] = 0

#     # Check if the user is already logged in
#     if 'logged_in' in session:
#         decrypted_data = session.get('decrypted_data')
#         decrypted_data_parts = decrypted_data.split(',')
#         username = decrypted_data_parts[0]
#         general_id = decrypted_data_parts[1]
#         position = decrypted_data_parts[2]

#         return render_template('sample.html', username=username, general_id=general_id, position=position)
    
#     # If the user is not logged in, attempt to decrypt the data
#     encrypted_data = request.args.get('data')
#     hex_passphrase = '3cd28375cbc0ad3e7540e3e0df98a411b643373819ee8bb60abb056c0425cc15'  # Replace with your hex passphrase

#     if encrypted_data:
#         try:
#             decrypted_data = my_decrypt(encrypted_data, hex_passphrase)

#             decrypted_data_parts = decrypted_data.split(',')
#             username = decrypted_data_parts[0]
#             general_id = decrypted_data_parts[1]
#             position = decrypted_data_parts[2]

#             session['decrypted_data'] = decrypted_data  # Store decrypted data in session
#             session['username'] = username  # Store decrypted username in session
#             session['general_id'] = general_id  # Store decrypted general_id in session
#             session['position'] = position  # Store decrypted position in session

#             session['logged_in'] = True  # Set session variable to indicate logged in
#         except Exception as e:
#             error_message = {"error": "Error decrypting data", "details": str(e)}
#             return jsonify(error_message), 500  # Return JSON response with error message and status code
#     else:
#         return "No data to decrypt"

#     decrypted_data = session.get('decrypted_data')
#     decrypted_data_parts = decrypted_data.split(',')
#     username = decrypted_data_parts[0]
#     general_id = decrypted_data_parts[1]
#     position = decrypted_data_parts[2]

#     return render_template('fr_page.html', username=username, general_id=general_id, position=position)

# if __name__ == "__main__":
#     app.run(debug=True)

# import secrets

# passphrase = secrets.token_hex(32)
# print(passphrase)



from functools import wraps
from flask import Flask, request, jsonify, render_template, session, redirect
import jwt

app = Flask(__name__)
app.secret_key = 'GAo2wWbWR2vM1BYexzAXs9QDuHXYkgKZ'

# Your JWT secret key
JWT_SECRET_KEY = 'your_jwt_secret_key'

# Custom decorator to check if user is logged in with JWT
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('jwt')  # Retrieve token from query parameter

        if not token:
            return jsonify({'message': 'Missing token'}), 401

        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            print(data)
            # Extract user information from the decoded token
            user_id = data['user_id']
            # general_id = data['general_id']
            # position = data['position']
            fullname = data['fullname']
            role_id = data['role_id']
            # ref_id = data['ref_id']
            device = data['device']
            system_token = data['system_token']
            token_id = data['token_id']
            exp = data['exp']

            session['user_id'] = user_id  
            # session['general_id'] = general_id  
            # session['position'] = position  
            session['fullname'] = fullname 
            session['role_id'] = role_id 
            # session['ref_id'] = ref_id 
            session['device'] = device 
            session['system_token'] = system_token 
            session['token_id'] = token_id 
            session['exp'] = exp 

            session['logged_in'] = True 

            # Set the user information in the session or perform additional actions as needed
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            print("Invalid token")
            return jsonify({'message': 'Invalid token'}), 401

       
        return f(*args, **kwargs)
    return decorated_function

# Example protected route using JWT
@app.route('/')
@jwt_required
def protected():
    user_id = session.get('user_id')
    # general_id = session.get('general_id')
    # position = session.get('position')
    fullname = session.get('fullname')
    role_id = session.get('role_id')
    # ref_id = session.get('ref_id')
    device = session.get('device')
    system_token = session.get('system_token')
    token_id = session.get('token_id')
    exp = session.get('exp')
    
    return render_template('sample.html', user_id=user_id, fullname=fullname, role_id=role_id, device=device, system_token=system_token, token_id=token_id, exp=exp)


# logout route 
@app.route('/logout', methods=['POST'])
def logout():
    session.clear() # Clear all session variables
    return redirect("http://localhost/dev_eguro/app/index.php") # Redirect the user to the specified URL

if __name__ == '__main__':
    app.run(debug=True)

