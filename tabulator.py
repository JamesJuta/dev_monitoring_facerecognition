from flask import Flask, render_template
from flaskext.mysql import MySQL
from datetime import date
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'facerecog_attendance_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

@app.route('/display_database_table')
def display_database_table():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%m-%d-%Y')
    current_time = current_datetime.strftime('%I:%M:%S %p')
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM time_log ORDER BY log_id desc")
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return render_template('tabulator_table.html', data=data, columns=columns, current_datetime=current_datetime, current_date=current_date, current_time=current_time)

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
