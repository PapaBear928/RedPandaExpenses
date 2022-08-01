from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
### auto generate by import.os and urandom(12).hex()
app.config['SECRET_KEY'] = 'f245bcb4fef64c9cf2f83238'
#app.config['SECRET_KEY'] = '11PandaRed22'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from App import routes



