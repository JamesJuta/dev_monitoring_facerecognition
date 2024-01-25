from flask_mysqldb import MySQL

mysql = MySQL()

def init_app(app):
    app.config['MYSQL_DATABASE_USER'] = 'your_username'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'your_password'
    app.config['MYSQL_DATABASE_DB'] = 'your_database_name'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'

    mysql.init_app(app)