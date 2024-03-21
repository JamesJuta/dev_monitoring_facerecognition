from pygame import mixer
from gtts import gTTS
from functools import wraps
from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify
from datetime import datetime
import os
from PIL import Image
import numpy as np
import jwt

import mysql.connector
import cv2
from db_connect import get_db_connection, close_db_connection

# imports for decrypting the data in the URL
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Define constants
JWT_SECRET_KEY = 'your_jwt_secret_key' # JWT SECRET KEY
DEV_E_GURO = "http://localhost/dev_eguro/app/index.php" # DEV_E_GURO url
CASCADE_PATH = "resources/haarcascade_frontalface_default.xml" # Path to cascade file for face detection
DATASET_PATH = "dataset/" # Path to the dataset folder where images are stored
BATCH_SIZE = 200 
MAX_ATTEMPTS = 5 # Number of maximum attempts in face register password
LOCKOUT_TIME = 60  # Lockout time in seconds

# get database connection from db_connect file
db_connect = get_db_connection() 
mycursor = db_connect.cursor()

# function for handling date-related operations.
def get_current_date_time():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%m-%d-%Y')
    current_time = current_datetime.strftime('%I:%M:%S %p')
    current_year = current_datetime.strftime('%Y')
    day_of_week = current_datetime.strftime('%A')
    return current_datetime, current_date, current_time, current_year, day_of_week

# text to speech function
def text_to_speech(message):
    tts = gTTS(text=message, lang='en')
    tts.save("tts_output.mp3")
    mixer.music.load("tts_output.mp3")
    mixer.music.play()

# play mp3 file 
def play_sound(file_name):
    try:
        mixer.music.load(f"sound/{file_name}")
        mixer.music.play()
        return True
    except Exception as e:
        print(f"Error during sound playback: {e}")
        return False

# login required decorator for routes that require user authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('jwt')  # Retrieve token from query parameter

        # if 'logged_in' not in session:
        #     return redirect(url_for('login', next=request.url))

        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        
        # if not token:
        #     return jsonify({'message': 'Missing token'}), 401

        # Check if token is not present in query parameters
        if not token:
            # Check if token is present in session
            token = session.get('jwt')

            # If token is still not present, return missing token error
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

            if exp is None:
                return jsonify({'message': 'Token has no expiration time'}), 401

            # Check if the token is expired
            current_time = datetime.utcnow().timestamp()
            if current_time > exp:
                # Clear all session variables
                session.clear()
                # return jsonify({'message': 'Expired token'}), 401
                return redirect(DEV_E_GURO)

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

            session['token'] = token 

            # Set the user information in the session or perform additional actions as needed
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            print("Invalid token")
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated_function

#  Generate dataset 
def generate_dataset(nbr):  
    face_classifier = cv2.CascadeClassifier(CASCADE_PATH)
 
    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
 
        if faces is ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face
 
    cap = cv2.VideoCapture(0)
 
    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]
 
    img_id = lastid
    max_imgid = img_id + 100    
    count_img = 0
 
    while True:
        ret, img = cap.read()
        if face_cropped(img) is not None:
            count_img += 1
            img_id += 1
            face = cv2.resize(face_cropped(img), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
 
            file_name_path = "dataset/"+nbr+"."+ str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count_img), (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

            query = "INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES (%s, %s)"
            values = (img_id, nbr)
            try:
                mycursor.execute(query, values)
                db_connect.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
 
            frame = cv2.imencode('.jpg', face)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
            if cv2.waitKey(1) == 13 or int(img_id) == int(max_imgid):
                break
                cap.release()
                cv2.destroyAllWindows()

# Train the classifier with images of a specific person
def train_classifier(nbr): 
    dataset_dir = "dataset"
 
    path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
    faces = []
    ids = []
 
    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])
 
        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)
 
    # Train the classifier and save
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
 
    message = "Images trained successfully!"
    return jsonify({'success': True, 'message': message, 'redirect': url_for('face_register')})


# Decryption function
def decrypt_data(encrypted_data, key, iv):
    # Ensure the key is the correct length
    key = key[:32]  # Trim to 32 bytes if longer
    iv_bytes = bytes.fromhex(iv) # Convert IV from hexadecimal string to bytes
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))

    # Unpad the decrypted data
    decrypted_data = unpad(decrypted_data, AES.block_size)

    return decrypted_data.decode('utf-8').strip()  # Remove leading/trailing whitespace
        

# Decrypt data function
# def decrypt_data(encrypted_data, key, iv):
#     cipher = AES.new(key, AES.MODE_CBC, iv)
#     decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))
#     unpadded_data = unpad(decrypted_data, AES.block_size)
#     return unpadded_data.decode('utf-8')