from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import mysql.connector

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0215@localhost/app'

db = SQLAlchemy(app)

connection = mysql.connector.connect(host = 'localhost',
                                         database = 'app',
                                         user = 'root',
                                         password = '0215')
cursor = connection.cursor()
                          

from app import routes
