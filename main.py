from flask import Flask
from flask_session import Session
from flaskext.mysql import MySQL
import functions.admin
import functions.auth

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'prediksi'
mysql.init_app(app)

functions.admin.init(app, mysql)
functions.auth.init(app, mysql)

if __name__ == '__main__':
    app.run(debug=True)
