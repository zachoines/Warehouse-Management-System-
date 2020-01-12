from flask import Flask
from config import Config


def main():
    app = Flask(__name__)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config.from_object(Config)
    from app import routes
    app.run(debug=True)
    

if __name__ == "__main__":
    main()