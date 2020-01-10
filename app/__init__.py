from flask import Flask
from config import Config


app = Flask(__name__)
app.config['ENV'] = 'development'
DEBUG = True
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config.from_object(Config)


from app import routes