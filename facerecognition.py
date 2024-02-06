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
 
app = Flask(__name__)
app.secret_key = 'GAo2wWbWR2vM1BYexzAXs9QDuHXYkgKZ'
mixer.init()
 
cnt = 0
pause_cnt = 0
justscanned = False
 
# database connection
db_connect = get_db_connection()
mycursor = db_connect.cursor()

current_datetime = datetime.now()
current_date = current_datetime.strftime('%m-%d-%Y')
current_time = current_datetime.strftime('%I:%M:%S %p')

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
    max_imgid = img_id + 20
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
 
    return redirect('/')
 
 
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
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
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
 
# route for the index page
@app.route('/')
def home():
    return render_template('fr_page.html')

# route for time log page
@app.route('/time_log', methods=['GET', 'POST'])
def time_log():
    correct_password = 'adminpassword'
    if 'password_attempts' not in session:
        session['password_attempts'] = 0

    if request.method == 'POST':
        password_attempt = request.form.get('password')

        if password_attempt == correct_password:
            # flash('Password is correct. Redirecting...', 'success')
            return redirect(url_for('face_register'))  
        else:
            session['password_attempts'] += 1
            flash('Incorrect password. Please try again.', 'error')
            
            if session['password_attempts'] == 5:
                flash('Maximum attempts reached. Please contact support.', 'error')
                session['password_attempts'] = 0  # Reset attempts after reaching the maximum
                

    return render_template('index_tabulator_ajax.html', current_datetime=current_datetime, current_date=current_date, current_time=current_time, password_attempts=session['password_attempts'])

# route for face register password
@app.route('/face_register_password', methods=['GET', 'POST'])
def face_register_password():
    correct_password = 'adminpassword'
    if request.method == 'POST':
        password_attempt = request.form.get('password')

        if password_attempt == correct_password:
            return redirect(url_for('face_register'))
        else:
            flash('Incorrect password. Please try again.', 'error')

    return render_template('password_form.html')

# route for face register page
@app.route('/face_register')
def face_register():
    sql = "SELECT id_no, name, time_added FROM users"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    return render_template('face_register.html', data=data)
 
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
    day_of_week = current_datetime.strftime('%A')  # Full name of the day (e.g., Monday)

    """Video streaming home page."""
    mycursor.execute("select a.accs_id, a.accs_prsn, b.name, a.accs_added "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id_no "
                     " where a.accs_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()

    if not data:
        return render_template('main.html', no_data=True)

    mycursor.execute("SELECT a.accs_prsn, b.name "
                     "FROM accs_hist a "
                     "LEFT JOIN users b ON a.accs_prsn = b.id_no "
                     "WHERE a.accs_date = curdate() "
                     "ORDER BY a.accs_added DESC "
                     "LIMIT 1")
    last_recognized_face = mycursor.fetchone()
 
    # Pass data, date, time, and day_of_week to the template
    return render_template('fr_page.html', data=data, current_date=current_date, current_time=current_time, day_of_week=day_of_week, last_recognized_face=last_recognized_face)

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


@app.route('/last_recognized_face', methods=['GET'])
def last_recognized_face():
    try:
        mycursor = db_connect.cursor(dictionary=True)

        # Assuming you have a column named 'log_id' as an auto-incrementing primary key
        mycursor.execute('SELECT * FROM time_log ORDER BY log_id DESC LIMIT 1')
        last_face_info = mycursor.fetchone()
        print(last_face_info)

        return jsonify(last_face_info)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify(error="Error fetching last recognized face information")

    finally:
        if 'connection' in locals() and db_connect.is_connected():
            mycursor.close()
            db_connect.close()
 
@app.route('/countTodayScan')
def countTodayScan():
    db_connect = get_db_connection()
    mycursor = db_connect.cursor() 
    mycursor.execute("SELECT count(*) FROM time_log WHERE DATE(datetime) = curdate()")
    row = mycursor.fetchone()
    rowcount = row[0]
    print(rowcount)
 
    return jsonify({'rowcount': rowcount})
 
@app.route('/loadData', methods = ['GET', 'POST'])  
def loadData():
    db_connect = get_db_connection()
    mycursor = db_connect.cursor()
 
    mycursor.execute("select a.accs_id, a.accs_prsn, b.name, date_format(a.accs_added, '%H:%i:%s') "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id_no "
                     " where a.accs_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()
 
    return jsonify(response = data)

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
        data_list = [{'value': str(item['students_id_no']), 'text': item['students_name']} for item in data]

        return jsonify(data_list)

    finally:
        # Close the cursor and connection
        close_db_connection(db_connect, mycursor)

# Internal Server Error
@app.errorhandler(401)
def error_401(e):
    return render_template("401.html"), 401

# Invalid URL
@app.errorhandler(404)
def error_404(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def error_500(e):
    return render_template("500.html"), 500
 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)