from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify, flash
import mysql.connector
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

# from flaskext.mysql import MySQL #pip install flask-mysql
# import pymysql
 
app = Flask(__name__)
mixer.init()
 
cnt = 0
pause_cnt = 0
justscanned = False
 
db_connect = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="facerecog_attendance_db"
)
mycursor = db_connect.cursor()

# mysql = MySQL()
   
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'facerecog_attendance_db'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

def text_to_speech(message):
    tts = gTTS(text=message, lang='en')
    tts.save("tts_output.mp3")
    mixer.music.load("tts_output.mp3")
    mixer.music.play()

def play_sound():
    mixer.music.load("error.mp3")
    mixer.music.play()
 
 
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
            cv2.putText(face, str(count_img), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            query = "INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES (%s, %s)"
            values = (img_id, nbr)
            mycursor.execute(query, values)
 
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
 
                mycursor.execute("select a.img_person, b.name, b.type_of_user "
                                 "  from img_dataset a "
                                 "  left join users b on a.img_person = b.id_no "
                                 " where img_id = " + str(id))
                row = mycursor.fetchone()   
                pnbr = row[0]
                pname = row[1]
                pskill = row[2]
                building_name= "jmc building"
                current_datetime = datetime.now()
                current_date = current_datetime.strftime('%m-%d-%Y')
                current_time = current_datetime.strftime('%I:%M:%S %p')
 
                if int(cnt) == 30:
                    cnt = 0
                    cv2.putText(img, pname + ' | ' + pskill, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
                    time.sleep(1)
                    text_to_speech("Time in success")

                    sql = "INSERT INTO `time_log` (`name`, `id_no`, `building_name`, `date`, `time`) VALUES (%s, %s, %s, %s, %s)"
                    values = (pname, pnbr, building_name, current_date, current_time)
                    mycursor.execute(sql, values)
                    db_connect.commit()

 
                    justscanned = True
                    pause_cnt = 0
 
            else:
                if not justscanned:
                    play_sound()
                    # text_to_speech("Face not recognized!")
                    cv2.putText(img, 'UNKNOWN', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.putText(img, "Face not recognize!", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                else:
                    cv2.putText(img, ' ', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,cv2.LINE_AA)
 
                if pause_cnt > 80:
                    justscanned = False
 
            coords = [x, y, w, h]
        return coords
 
    def recognize(img, clf, faceCascade):
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
 
 
@app.route('/')
def home():
    return render_template('fr_page.html')

@app.route('/time_log')
def time_log():
    return render_template('time_log2.html')


@app.route('/face_register_password', methods=['GET', 'POST'])
def face_register_password():
    correct_password = 'adminpassword'
    if request.method == 'POST':
        password_attempt = request.form.get('password')

        if password_attempt == correct_password:
            return redirect(url_for('addprsn'))
        else:
            flash('Incorrect password. Please try again.', 'error')

    return render_template('password_form.html')

@app.route('/face_register')
def face_register():
    sql = "SELECT id_no, name, type_of_user, time_added FROM users"
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
 
@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    prsnbr = request.form.get('txtnbr')
    prsname = request.form.get('txtname')
    prsskill = request.form.get('optskill')

    # face registration details will go to recently added users with face recognition
    #query should be using join statements to join the table of full info of the user and the table for enrollement status and notice
    
    sql = "INSERT INTO `users` (`id_no`, `name`, `type_of_user`) VALUES (%s, %s, %s)"
    values = (prsnbr, prsname, prsskill)
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
    mycursor.execute("select a.accs_id, a.accs_prsn, b.name, b.type_of_user, a.accs_added "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id_no "
                     " where a.accs_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()

    if not data:
        return render_template('main.html', no_data=True)

    mycursor.execute("SELECT a.accs_prsn, b.name, b.type_of_user "
                     "FROM accs_hist a "
                     "LEFT JOIN users b ON a.accs_prsn = b.id_no "
                     "WHERE a.accs_date = curdate() "
                     "ORDER BY a.accs_added DESC "
                     "LIMIT 1")
    last_recognized_face = mycursor.fetchone()
 
    # Pass data, date, time, and day_of_week to the template
    return render_template('fr_page.html', data=data, current_date=current_date, current_time=current_time, day_of_week=day_of_week, last_recognized_face=last_recognized_face)


# @app.route("/ajaxfile",methods=["POST","GET"])
# def ajaxfile():
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         if request.method == 'POST':
#             draw = request.form['draw'] 
#             row = int(request.form['start'])
#             rowperpage = int(request.form['length'])
#             searchValue = request.form["search[value]"]
#             print(draw)
#             print(row)
#             print(rowperpage)
#             print(searchValue)
 
#             ## Total number of records without filtering
#             # sql = "select log_id, name, id_no,building_name, time, date from time_log ORDER BY log_id DESC"
#             # cursor.execute(sql)
#             cursor.execute("select count(*) as allcount from time_log where date = curdate() ORDER BY log_id DESC")
#             rsallcount = cursor.fetchone()
#             totalRecords = rsallcount['allcount']
#             print(totalRecords) 
 
#             ## Total number of records with filtering
#             likeString = "%" + searchValue +"%"
#             cursor.execute("SELECT count(*) as allcount from time_log WHERE name LIKE %s OR time LIKE %s OR date LIKE %s OR building_name LIKE %s OR id_no LIKE %s", (likeString, likeString, likeString, likeString, likeString))
#             rsallcount = cursor.fetchone()
#             totalRecordwithFilter = rsallcount['allcount']
#             print(totalRecordwithFilter) 
 
#             ## Fetch records
#             if searchValue=='':
#                 cursor.execute("SELECT * FROM time_log ORDER BY log_id DESC limit %s, %s;", (row, rowperpage))
#                 # cursor.execute("SELECT * FROM time_log ORDER BY date asc limit %s, %s;", (row, rowperpage))
#                 timeloglist = cursor.fetchall()
#             else:        
#                 cursor.execute("SELECT * FROM time_log WHERE name LIKE %s OR time LIKE %s OR date LIKE %s OR building_name LIKE %s OR id_no LIKE %s limit %s, %s;", (likeString, likeString, likeString, likeString, likeString, row, rowperpage))
#                 timeloglist = cursor.fetchall()
    
#             data = []
#             for row in timeloglist:
#                 data.append({
#                     'name': row['name'],
#                     'id_no': row['id_no'],
#                     'building_name': row['building_name'],
#                     'time': row['time'],
#                     'date': row['date'],
#                 })
 
#             response = {
#                 'draw': draw,
#                 'iTotalRecords': totalRecords,
#                 'iTotalDisplayRecords': totalRecordwithFilter,
#                 'aaData': data,
#             }
#             print(response)
#             return jsonify(response)
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close() 
#         conn.close()
 
 
@app.route('/countTodayScan')
def countTodayScan():
    db_connect = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="facerecog_attendance_db"
    )
    mycursor = db_connect.cursor()
 
    mycursor.execute("select count(*) "
                     "  from accs_hist "
                     " where accs_date = curdate() ")
    row = mycursor.fetchone()
    rowcount = row[0]
 
    return jsonify({'rowcount': rowcount})
 
 
@app.route('/loadData', methods = ['GET', 'POST'])
def loadData():
    db_connect = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="facerecog_attendance_db"
    )
    mycursor = db_connect.cursor()
 
    mycursor.execute("select a.accs_id, a.accs_prsn, b.name, b.type_of_user, date_format(a.accs_added, '%H:%i:%s') "
                     "  from accs_hist a "
                     "  left join users b on a.accs_prsn = b.id_no "
                     " where a.accs_date = curdate() "
                     " order by 1 desc")
    data = mycursor.fetchall()
 
    return jsonify(response = data)
 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)