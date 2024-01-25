#app.py
from flask import Flask, request, render_template, jsonify, json
from flaskext.mysql import MySQL #pip install flask-mysql
import pymysql
  
app = Flask(__name__)
    
mysql = MySQL()
   
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'facerecog_attendance_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
  
@app.route('/')
def home():
    return render_template('tabulator_table.html')
 
@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)
 
            ## Total number of records without filtering
            # sql = "select log_id, name, id_no,building_name, time, date from time_log ORDER BY log_id DESC"
            # cursor.execute(sql)
            cursor.execute("select count(*) as allcount from time_log where date = curdate() ORDER BY log_id DESC")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords) 
 
            ## Total number of records with filtering
            likeString = "%" + searchValue +"%"
            cursor.execute("SELECT count(*) as allcount from time_log WHERE name LIKE %s OR time LIKE %s OR date LIKE %s OR building_name LIKE %s OR id_no LIKE %s", (likeString, likeString, likeString, likeString, likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter) 
 
            ## Fetch records
            if searchValue=='':
                cursor.execute("SELECT * FROM time_log ORDER BY log_id DESC limit %s, %s;", (row, rowperpage))
                # cursor.execute("SELECT * FROM time_log ORDER BY date asc limit %s, %s;", (row, rowperpage))
                timeloglist = cursor.fetchall()
            else:        
                cursor.execute("SELECT * FROM time_log WHERE name LIKE %s OR time LIKE %s OR date LIKE %s OR building_name LIKE %s OR id_no LIKE %s limit %s, %s;", (likeString, likeString, likeString, likeString, likeString, row, rowperpage))
                timeloglist = cursor.fetchall()
    
            data = []
            for row in timeloglist:
                data.append({
                    'name': row['name'],
                    'id_no': row['id_no'],
                    'building_name': row['building_name'],
                    'time': row['time'],
                    'date': row['date'],
                })
 
            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()



# @app.route('/')
# def index():
#    src = os.path.join(app.config['UPLOAD_FOLDER'], 'file.xlsx')
#    df = pd.read_excel(src, engine='openpyxl')
#    return render_template('index.html', data=df.to_dict(orient='records')
 
if __name__ == "__main__":
    app.run()