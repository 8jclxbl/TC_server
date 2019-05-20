import dash
from flask import Flask
from models import *

server = Flask(__name__)
external_stylesheets = ['./static/total.css'] 
app = dash.Dash(server = server,external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server.config.from_object('config')
