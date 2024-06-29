import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_CONFIG') or 'DevelopmentConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)