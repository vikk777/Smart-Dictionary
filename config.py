import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig():
	"""Application config"""
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
	