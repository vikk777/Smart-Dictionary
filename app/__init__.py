from flask import Flask
<<<<<<< HEAD
# from flask_migrate import Migrate, MigrateCommand
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os, config
=======
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
# from flask_login import LoginManager
import config
>>>>>>> d2557fa81ab23f1b2c84428f3e96f917ea36f83d

app = Flask(__name__)
app.config.from_object('config')

# Initial extensions
<<<<<<< HEAD
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
=======
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# login_manager = LoginManager(app)
# login_manager = login_view = 'login'
>>>>>>> d2557fa81ab23f1b2c84428f3e96f917ea36f83d

from app import views, database
