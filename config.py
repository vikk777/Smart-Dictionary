import os

appDir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
    'mysql+pymysql://root:@localhost/smart_dict'
# 'mysql+pymysql://root:@localhost/temp'
# SQLALCHEMY_ECHO = True
SQLALCHEMY_ENGINE_OPTIONS = {  # 'pool_recycle': 280,
    #'pool_timeout': 100,
    'pool_pre_ping': True}
