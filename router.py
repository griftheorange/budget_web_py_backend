from flask import Flask
from flask_cors import CORS
from constants import ColumnSets
from loader import *
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

@app.route('/data')
def data_to_json():
    df = load_excel_file(ColumnSets.BUDGET_STD)
    return df.to_json()
    