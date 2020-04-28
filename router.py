from flask import Flask
from loader import *
from column_sets import ColumnSets
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

@app.route('/data')
def data_to_json():
    df = load_excel_file()
    return df.to_json()
    