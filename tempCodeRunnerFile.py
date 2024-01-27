  # if table is not None and table != '':
            
        #     connection = get_db_connection()
        #     cursor = connection.cursor(dictionary=True)

        #     # Use the user_id in the SQL query
        #     sql = "SELECT DATE(datetime) AS date_only, TIME(datetime) AS time_only, name, building_name FROM time log ORDER BY log_id desc WHERE date_only = "
        #     # print(sql)
        #     cursor.execute(sql)
        #     # cursor.execute('SELECT date, time, name, building_name FROM time_log ORDER BY log_id desc')
        #     data = cursor.fetchall()
        #     return jsonify(data=data)
        # else:
        #     ret