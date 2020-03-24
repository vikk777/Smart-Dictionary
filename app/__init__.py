from flask import Flask
# from flask_migrate import Migrate, MigrateCommand
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
import os, config

app = Flask(__name__)
app.config.from_object('config')

# Initial extensions
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login_manager = LoginManager(app)
# login_manager = login_view = 'login'

# import views
from app import views