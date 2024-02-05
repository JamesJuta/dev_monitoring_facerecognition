if 'connection' in locals() and db_connect.is_connected():
            mycursor.close()
            db_connect.close()