from flask import Flask
from flask_cors import CORS

from controllers.line_graph import getLineData

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

@app.route('/line_data')
def data_to_json():
    return getLineData()
    