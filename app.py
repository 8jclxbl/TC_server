import dash
from flask import Flask

server = Flask(__name__)
external_stylesheets = ['./static/total.css'] 
external_scripts = ['./static/plotly-1.47.0.min.js']
app = dash.Dash(server = server,external_stylesheets=external_stylesheets,external_scripts=external_scripts)
app.config.suppress_callback_exceptions = True
server.config.from_object('config')
