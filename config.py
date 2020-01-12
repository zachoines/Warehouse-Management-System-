import os

# This class contains a secret key combination for login
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password'
    DEBUG = True
    TESTING = True