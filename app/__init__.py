from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path='/static')

from app import views

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\project\\Test_xray\\chestxray\\app\\static\\db\\database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

Bootstrap(app)
db = SQLAlchemy(app)
#pip freeze > requirements.txt / to generate requirements file