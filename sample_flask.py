from flask import Flask, session, request, render_template
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem (you can change this to use other session backends)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
Session(app)

@app.route('/')
def index():

    # Retrieve username and password from query parameters
    # username = request.args.get('username')
    # password = request.args.get('password')

    # Retrieve username and password from session
    username = session.get('username')
    password = session.get('password')

    # Here you can use the username and password to display user information or perform other actions
    return render_template("sample.html", username=username)

if __name__ == '__main__':
    app.run(debug=True)
