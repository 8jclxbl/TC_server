import dash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *

server = Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 
app = dash.Dash(server = server,external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True 
server.config.from_object('config')
db = SQLAlchemy(server)