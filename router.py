from flask import Flask
from flask_cors import CORS

from constants import *
from controllers.json_parsers import *

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

@app.route('/line_data/<filename>', methods=["GET"])
def line_data(filename):
    return fetch_line_data(filename, cols=ColumnSets.BUDGET_STD)

@app.route('/data/<filename>', methods=["GET"])
def data(filename):
    return fetch_data(filename)

@app.route('/data', methods=["POST"])
def post_data():
    return "Hello"

@app.route('/print_csv')
def print_csv():
    fetch_print_csv()
    return "Printed"