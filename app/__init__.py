from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import config

app = Flask(__name__)
app.config.from_object('config')

# Initial extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
loginManager = LoginManager(app)
bootstrap = Bootstrap(app)

from app import views
from app.sderrors import handlers
