@app.route('/get_data', methods=['GET'])
# def get_data():
#     try:
#         # Get the value of the 'user_id' parameter from the GET request
#         table = request.args.get('table')
#         date_format= "%Y-%m-%d"

#         # Check if 'user_id' is provided and is not empty
#         if table is not None and table != '':

           
#             connection = get_db_connection()
#             cursor = connection.cursor(dictionary=True)

#             # SELECT DATE(datetime) AS date_only, TIME(datetime) AS time_only, name, building_name FROM time_log WHERE DATE_FORMAT(datetime,"%Y-%m-%d") >= '2024-01-01' AND DATE_FORMAT(datetime,"%Y-%m-%d") <= '2024-01-01' ORDER BY `date_only`  DESC;

#             # sql = 'SELECT DATE(datetime) AS date_only, TIME(datetime) AS time_only, name, building_name FROM time_log WHERE DATE_FORMAT(datetime,%s) >= %s AND DATE_FORMAT(datetime,%s) <= %s ORDER BY `date_only`  DESC'
#             # values = [date_format, start_date, end_date, date_format]
#             # cursor.execute(sql, values)

#             # Use the user_id in the SQL query
#             # sql = "SELECT DATE(datetime) AS date_only, TIME(datetime) AS time_only, name, building_name FROM time log  ORDER BY log_id desc"
#             # cursor.execute(sql)
#             cursor.execute('SELECT date, time, name, building_name FROM time_log ORDER BY log_id desc')
#             data = cursor.fetchall()
#             return jsonify(data=data)
#         else:
#             return jsonify(error="User ID parameter is missing or empty")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if 'connection' in locals() and connection.is_connected():
#             cursor.close()
#             connection.close()
#     return jsonify(data=[])