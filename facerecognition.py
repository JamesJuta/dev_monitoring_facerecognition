from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify, flash
import mysql.connector
from db_connect import get_db_connection, close_db_connection
import cv2
from PIL import Image
import numpy as np
import os
import time  
from datetime import date
from datetime import datetime
from gtts import gTTS
import os
from pygame import mixer
import dlib

# imports for decrypting the data in the URL
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
 
app = Flask(__name__)
app.secret_key = 'GAo2wWbWR2vM1BYexzAXs9QDuHXYkgKZ'
mixer.init()

camera = cv2.VideoCapture(0)
capture_in_progress = False
image_count = 0
total_images = 100  # Total images to capture
detector = dlib.get_frontal_face_detector()
face_cascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
 
cnt = 0
pause_cnt = 0
justscanned = False
 
# get database connection from db_connect file
db_connect = get_db_connection()
mycursor = db_connect.cursor()

current_datetime = datetime.now()
current_date = current_datetime.strftime('%m-%d-%Y')
current_time = current_datetime.strftime('%I:%M:%S %p')
current_year = current_datetime.strftime('%Y')
day_of_week = current_datetime.strftime('%A')  # Full name of the day (e.g., Monday)

# Number of maximum attempts
MAX_ATTEMPTS = 5
# Lockout time in seconds
LOCKOUT_TIME = 60  # 3 minutes in seconds

# Keeping track of attempts and last attempt time
attempt_count = 0
last_attempt_time = None

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
 
 
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generate dataset >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def generate_dataset(nbr):
    face_classifier = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
 
    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor=1.3
        # Minimum neighbor = 5
 
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
 
 
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Train Classifier >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/train_classifier/<nbr>')
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
 
    # return redirect('/')
    # Display success message using SweetAlert
    message = "Images trained successfully!"
    return jsonify({'success': True, 'message': message, 'redirect': url_for('face_register')})
 
 
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Face Recognition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def face_recognition():  # generate frame by frame from camera
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
 
        global justscanned
        global pause_cnt
 
        pause_cnt += 1
 
        coords = []
 
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))
 
            if confidence > 70 and not justscanned:
                global cnt
                cnt += 1
 
                n = (100 / 30) * cnt
                # w_filled = (n / 100) * w
                w_filled = (cnt / 30) * w
 
                cv2.putText(img, str(int(n))+' %', (x + 20, y + h + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (153, 255, 255), 2, cv2.LINE_AA)
 
                cv2.rectangle(img, (x, y + h + 40), (x + w, y + h + 50), color, 2)
                cv2.rectangle(img, (x, y + h + 40), (x + int(w_filled), y + h + 50), (153, 255, 255), cv2.FILLED)
 
                mycursor.execute("select a.img_person, b.name "
                                 "  from img_dataset a "
                                 "  left join users b on a.img_person = b.id_no "
                                 " where img_id = " + str(id))
                row = mycursor.fetchone()   
                pnbr = row[0]
                pname = row[1]
                building_name= "jmc building"
                current_datetime = datetime.now()
                current_date = current_datetime.strftime('%m-%d-%Y')
                current_time = current_datetime.strftime('%I:%M:%S %p')
 
                if int(cnt) == 30:
                    cnt = 0
                    cv2.putText(img, pname, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
                    time.sleep(1)
                    play_sound("time_in_success.mp3")

                    sql = "INSERT INTO `time_log` (`name`, `id_no`, `building_name`, `date`, `time`) VALUES (%s, %s, %s, %s, %s)"
                    values = (pname, pnbr, building_name, current_date, current_time)
                    mycursor.execute(sql, values)
                    db_connect.commit()

 
                    justscanned = True
                    pause_cnt = 0
 
            else:
                if not justscanned:
                    play_sound("error.mp3")
                    cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.putText(img, "Face not recognize!", (20, 350),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                else:
                    cv2.putText(img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,cv2.LINE_AA)
 
                if pause_cnt > 80:
                    justscanned = False
 
            coords = [x, y, w, h]
        return coords
 
    def recognize(img, clf, faceCascade):
        img = cv2.flip(img, 1)
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
        return img
 
    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")
 
    wCam, hCam = 400, 400
 
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
 
    while True:
        ret, img = cap.read()
        img = recognize(img, clf, faceCascade)
 
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
 
        key = cv2.waitKey(1)
        if key == 27:
            break

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

# route for the index page
@app.route('/')
def home():
    session.pop('authenticated', None)
    if 'attempt_count' not in session:
        session['attempt_count'] = 0

    # encrypted_data = request.args.get('data')
    # hex_iv = request.args.get('iv')

    # if encrypted_data and hex_iv:
    #     # Decrypt the data using the same key used in PHP
    #     decryptionKey = b'g5K8Ht+6oCOOG8IJnZIoR59Doa8shfBjqRvvhb9yIGU='
    #     try:
    #         decrypted_username = decrypt_data(encrypted_data, decryptionKey, hex_iv)
    #         session['username'] = decrypted_username  # Store decrypted username in session
    #         return render_template('fr_page.html', username=decrypted_username)
    #     except Exception as e:
    #         return f"Error decrypting data: {str(e)}"
    # else:
    #     return "No data to decrypt"
    
    return render_template('fr_page.html', current_year=current_year)

# route for time log page
@app.route('/time_log', methods=['GET', 'POST'])
def time_log():

    # decrypted_username = session.get('username')

    session.pop('authenticated', None)
    if 'attempt_count' not in session:
        session['attempt_count'] = 0          

    return render_template('index_tabulator_ajax.html', current_datetime=current_datetime, current_date=current_date, current_time=current_time, current_year=current_year)
    # return render_template('index_tabulator_ajax.html', current_datetime=current_datetime, current_date=current_date, current_time=current_time, current_year=current_year, username=decrypted_username)


# Middleware function to check if the user is authenticated before accessing the face register page
@app.before_request
def check_authentication():
    if request.endpoint == 'face_register' and 'authenticated' not in session:
        return redirect(url_for('face_register_password'))

# route for removing the flag of authenticated session variable
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('home'))

@app.route('/face_register_password', methods=['GET', 'POST'])
def face_register_password():
    return render_template('face_register_password.html', error=None)


# route for validating the password when going to the face register page
@app.route('/validate_password', methods=['POST'])
def validate_password():
    if 'attempt_count' not in session:
        session['attempt_count'] = 0

    # Check if the button has been locked out
    if 'last_attempt_time' in session and time.time() - session['last_attempt_time'] < LOCKOUT_TIME:
        return jsonify({'success': False, 'message': f'You are locked out. Please try again in {LOCKOUT_TIME // 60} minutes.'})

    # Get password from the form
    password = request.form['password']

    # Check if password is correct
    if password == 'adminpassword':
        session['attempt_count'] = 0  # Reset attempt count
        session['authenticated'] = True
        return jsonify({'success': True, 'redirect': url_for('face_register')})
    else:
        session['attempt_count'] += 1
        # Check if max attempts reached
        if session['attempt_count'] >= MAX_ATTEMPTS:
            session['last_attempt_time'] = time.time()  # Set lockout time
            session['attempt_count'] = 0  # Reset attempt count
            return jsonify({'success': False, 'lockout': True, 'message': f'You are locked out for {LOCKOUT_TIME // 60} minutes.', 'attempts': session['attempt_count']})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password. Please try again.', 'attempts': session['attempt_count']})

# route for face register page
@app.route('/face_register')
def face_register():
    # decrypted_username = session.get('username')
    # return render_template('face_register.html', current_year=current_year, username=decrypted_username)
    return render_template('face_register.html', current_year=current_year)
 
@app.route('/addprsn')
def addprsn():
    mycursor.execute("select ifnull(max(id_no) + 1, 101) from users")
    row = mycursor.fetchone()
    nbr = row[0]
    # print(int(nbr))
 
    return render_template('addprsn.html', newnbr=int(nbr))

#
@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    prsnbr = request.form.get('txtnbr')
    prsname = request.form.get('txtname')

    # sql1= "SELECT students_id_no, students_name FROM enrolled_students WHERE students_id_no=%s"
    # mycursor.execute(sql1, prsnbr)

    # face registration details will go to recently added users with face recognition
    #query should be using join statements to join the table of full info of the user and the table for enrollement status and notice
    
    sql = "INSERT INTO `users` (`id_no`, `name`) VALUES (%s, %s)"
    values = (prsnbr, prsname)
    mycursor.execute(sql, values)
    
    db_connect.commit()
 
    # return redirect(url_for('home'))
    return redirect(url_for('vfdataset_page', prs=prsnbr))
 
@app.route('/vfdataset_page/<prs>')
def vfdataset_page(prs):
    return render_template('gendataset.html', prs=prs)
 
@app.route('/vidfeed_dataset/<nbr>')
def vidfeed_dataset(nbr):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_dataset(nbr), mimetype='multipart/x-mixed-replace; boundary=frame')
 
# route for the video feed in the face recognition
@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
@app.route('/fr_page')
def fr_page():
    # Get current date and time
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    current_time = current_datetime.strftime('%H:%M:%S %p')
 
    # Pass data, date, time, and day_of_week to the template
    return render_template('fr_page.html', current_date=current_date, current_time=current_time, day_of_week=day_of_week)

# route for getting the data for the time log table
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        table = request.args.get('table')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        mycursor = db_connect.cursor(dictionary=True)

        if table is not None and table != '':
            if start_date and end_date:
                # If start_date and end_date are provided, filter by date range
                sql = 'SELECT date, time, name, building_name FROM time_log WHERE DATE(datetime) >= %s AND DATE(datetime) <= %s ORDER BY log_id DESC'
                values = [start_date, end_date]
                mycursor.execute(sql, values)
            else:
                # If start_date and end_date are not provided, fetch all data
                mycursor.execute('SELECT date, time, name, building_name FROM time_log where DATE(datetime) = curdate() ORDER BY log_id DESC')

            data = mycursor.fetchall()
            return jsonify(data=data)
        else:
            return jsonify(error="Table parameter is missing or empty")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and db_connect.is_connected():
            mycursor.close()
            db_connect.close()
    return jsonify(data=[])

# get recently added users
@app.route('/get_recently_added_users_data', methods=['GET'])
def get_recently_added_users_data():
    try:
        # Get the value of the 'user_id' parameter from the GET request
        table = request.args.get('table')

        # Check if 'user_id' is provided and is not empty
        if table is not None and table != '':
            mycursor = db_connect.cursor(dictionary=True)

            # Use the user_id in the SQL query
            sql = 'SELECT id_no, name, time_added FROM users ORDER BY time_added DESC'
            mycursor.execute(sql)
            # mycursor.execute('SELECT general_id,f_name FROM users WHERE user_id = %s', (table,))
            data = mycursor.fetchall()
            return jsonify(data=data)
        else:
            return jsonify(error="User ID parameter is missing or empty")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and db_connect.is_connected():
            mycursor.close()
            db_connect.close()
    return jsonify(data=[])
 
@app.route('/countTodayScan')
def countTodayScan():
    db_connect = get_db_connection()
    mycursor = db_connect.cursor()
    sql = 'SELECT count(*) FROM time_log WHERE DATE(datetime) = curdate()' 
    mycursor.execute(sql)
    row = mycursor.fetchone()
    rowcount = row[0]
    # print(rowcount)
 
    return jsonify({'rowcount': rowcount})
 
@app.route('/loadData', methods = ['GET', 'POST'])  
def loadData():
    db_connect = get_db_connection()
    mycursor = db_connect.cursor()
    
    sql = 'SELECT * FROM time_log WHERE DATE(datetime) = curdate() ORDER BY log_id DESC'
    mycursor.execute(sql)
    # mycursor.execute("select a.accs_id, a.accs_prsn, b.name, date_format(a.accs_added, '%H:%i:%s') "
    #                  "  from accs_hist a "
    #                  "  left join users b on a.accs_prsn = b.id_no "
    #                  " where a.accs_date = curdate() "
    #                  " order by 1 desc")
    # data = mycursor.fetchall()
    
    data=mycursor.fetchone()
    if data:
        # Convert data to a dictionary
        data_dict = {
            'log_id': data[0],
            'name': data[1],
            'id_no': data[2],
            'building_name': data[3],
            'time': data[4],
            'date': data[5],
        }
        
        return jsonify(response=data_dict)
    else:
        return jsonify(response=None)

# route for getting the enrolled users and will be displayed in the selectize input
@app.route('/get_enrolled_users_data', methods=['GET'])
def get_enrolled_users_data():
    db_connect = get_db_connection()
    mycursor = db_connect.cursor(dictionary=True)
    try:
        # Fetch data from the database
        query = "SELECT students_id_no, students_name FROM enrolled_students"
        mycursor.execute(query)
        data = mycursor.fetchall()

        # Convert data to a list of dictionaries
        data_list = [{'value': str(item['students_id_no']), 'text': item['students_id_no']} for item in data]

        return jsonify(data_list)

    finally:
        # Close the cursor and connection
        close_db_connection(db_connect, mycursor)

# Internal Server Error
@app.errorhandler(401)
def error_401(e):
    play_sound("error_401.mp3")
    return render_template("401.html"), 401

# Invalid URL
@app.errorhandler(404)
def error_404(e):
    # play_sound("error_404.mp3")   
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def error_500(e):
    play_sound("error_500.mp3")
    return render_template("500.html"), 500


def generate_frames():
    global image_count, total_images, capture_in_progress
    # Initialize frame rate calculation
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()

    while True:
        success, frame = camera.read()
        t1 = cv2.getTickCount()  # Get tick count for frame rate calculation
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)  # Mirror the frame horizontally
            frame_width, frame_height = frame.shape[1], frame.shape[0]  # Get frame dimensions

            # Get the current time in hour, minute, and second format
            current_time = time.strftime('%H:%M:%S', time.localtime())

            # Perform face detection on the frame
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = detector(frame, 0)
            
            for face in faces:
                # Get the coordinates of the detected face
                face_left, face_top, face_right, face_bottom = face.left(), face.top(), face.right(), face.bottom()
                
                # Check if the face is out of range based on the frame size
                out_of_range = face_left < 0 or face_top < 0 or face_right > frame_width or face_bottom > frame_height
                
                if out_of_range:
                    # Change the color to red for out-of-range face detection
                    cv2.rectangle(frame, (face_left, face_top), (face_right, face_bottom), (0, 0, 255), 2)
                    cv2.putText(frame, 'Face out of range', (face_left, face_bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    # Draw rectangles around detected faces (normal)
                    cv2.rectangle(frame, (face_left, face_top), (face_right, face_bottom), (255, 255, 255), 2)
 

            if capture_in_progress:
                progress = int((image_count / total_images) * 100)  # Calculate progress percentage

                # Draw a smaller progress bar with adjusted height
                bar_width = int((progress / 100) * 300)  # Width of the progress bar (maximum: 300)
                bar_height = 10  # Height of the progress bar
                cv2.rectangle(frame, (20, 450 - bar_height), (20 + bar_width, 450), (214,82,51), -1)
                cv2.putText(frame, f'Progress: {progress}%', (20, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Display the current time in hour, minute, second format
            cv2.putText(frame, f'Time: {current_time}', (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Display the frame with bounding boxes and calculated frame rate
            cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Display the number of faces in the current frame
            num_faces_text = f'No. of Faces in frame: {len(faces)}'
            cv2.putText(frame, num_faces_text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            t2 = cv2.getTickCount()  # Get tick count for frame rate calculation
            time1 = (t2 - t1) / freq  # Calculate time difference
            frame_rate_calc = 1 / time1  # Calculate frame rate

            # Encoding and yielding frames with detected faces
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

####
@app.route('/video_feed_face_register')
def video_feed_face_register():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/register', methods=['GET', 'POST'])
def register():

    global image_count, total_images, capture_in_progress
    face_classifier = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor=1.3
        # Minimum neighbor = 5
 
        if faces is ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face
    
    mycursor.execute("select ifnull(max(img_id), 0) from img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]
 
    img_id = lastid
    max_imgid = img_id + 20
    count_img = 0
    
    
    if not capture_in_progress:
        capture_in_progress = True
        image_count = 0
    if request.method == 'POST':
        nbr = request.form['txtnbr']
        prsname = request.form.get('txtname')

        sql = "INSERT INTO `users` (`id_no`, `name`) VALUES (%s, %s)"
        values = (nbr, prsname)
        mycursor.execute(sql, values)
        
        db_connect.commit()

        while capture_in_progress and image_count < total_images:
            success, frame = camera.read()
            if success:

                if face_cropped(frame) is not None:
                    image_count += 1
                    img_id += 1
                    face = cv2.resize(face_cropped(frame), (200, 200))
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


        if capture_in_progress:
            capture_in_progress = False

            train_classifier(nbr)

            message = "Images captured successfully!"
            return jsonify({'success': True, 'message': message})
        else:
            return 'Failed to capture image.'

    # return render_template('register.html')   
    return jsonify({'success': True, 'message': message})

if __name__ == "__main__":
    # play_sound("initializing.mp3")
    app.run(host='127.0.0.1', port=5000, debug=True)