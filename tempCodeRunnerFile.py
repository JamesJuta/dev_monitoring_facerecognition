# If start_date and end_date are not provided, fetch all data
                mycursor.execute('SELECT date, time, name, building_name FROM time_log ORDER BY log_id DESC')