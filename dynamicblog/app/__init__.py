from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# This setting tells flask log in which function is used to deal with log in.
# If user clicks on other pages (if login required is set), they will be redirected to login?next=/index.
# if login_view is defined to be 'register', user will be redirected to register page instead
login.login_view = 'login'

from app import routes, models
