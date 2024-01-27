# example tabulator for time_log table 

from flask import Flask, render_template, jsonify, request, redirect, url_for
import mysql.connector
from datetime import datetime
app = Flask(__name__)

# Replace these values with your database credentials
db_host = "localhost"
db_user = "root"
db_name = "facerecog_attendance_db"
db_password = ""

# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,   
        database=db_name
    )

current_datetime = datetime.now()
current_date = current_datetime.strftime('%m-%d-%Y')
current_time = current_datetime.strftime('%I:%M:%S %p')
initial_date_range = f'{current_date}@{current_date}'

# Route to display data from the database
@app.route('/')
def index():
    return render_template('index_tabulator_ajax.html', current_datetime=current_datetime, current_date=current_date, current_time=current_time, initial_date_range=initial_date_range)

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        table = request.args.get('table')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if table is not None and table != '':
            if start_date and end_date:
                # If start_date and end_date are provided, filter by date range
                sql = 'SELECT date, time, name, building_name FROM time_log WHERE DATE(datetime) >= %s AND DATE(datetime) <= %s ORDER BY log_id DESC'
                values = [start_date, end_date]
                cursor.execute(sql, values)
            else:
                # If start_date and end_date are not provided, fetch all data
                cursor.execute('SELECT date, time, name, building_name FROM time_log ORDER BY log_id DESC')

            data = cursor.fetchall()
            return jsonify(data=data)
        else:
            return jsonify(error="Table parameter is missing or empty")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
    return jsonify(data=[])
    



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)