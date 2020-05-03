from flask import Flask, request
from flask_cors import CORS

from os import listdir

from constants import *
from controllers.json_parsers import JSONParsers as JSON
from controllers.data_handlers import DataHandlers as DH

app = Flask(__name__)
CORS(app)

# All computation other than non-null checks done through data_handler and json_parsers class
# Calls go to to Data-Handler through json parser class if a json object needs to be returned
@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

# just for testing and file listing, not necessarily a planned fetch yet
@app.route('/data', methods=['GET'])
def data_index():
    print(listdir('resources'))
    html = get_filenames()
    return html

@app.route('/data/<filename>', methods=["GET"])
def data(filename):
    cols = ColumnSets.BUDGET_ALL
    return JSON.fetch_data(filename, cols=cols)

#saves sent file to proper directory then loads in data
#inserts to data.p and returns
@app.route('/data', methods=["POST"])
def post_data():
    file = request.files['file']
    if(file):
        return JSON.save_and_insert_file(file)
    return "Hello"

# resets data.p based on source xl file
@app.route('/reset')
def reset_pickle():
    DH.reset_pickle()
    return "Reset"


#####################################################################
# Outdated, for now I'll send up both data and line data in single fetch
# Through '/data/<filename>' route
# @app.route('/line_data/<filename>', methods=["GET"])
# def line_data(filename):
#     cols = ColumnSets.BUDGET_ALL
#     return JSON.fetch_line_data(filename, cols=cols)
#####################################################################

#for testing
@app.route('/print_csv')
def print_csv():
    DH.load_and_print_csv()
    return "Printed"

#helper funciton for /data index route
def get_filenames():
    html = "<ul>"
    for filename in listdir('resources'):
        html += "<li>" + filename + "</li>"
        if(filename == "csv"):
            html += "<ul>"
            for filename in listdir('resources/csv'):
                html += "<li>" + filename + "</li>"
            html += "</ul>"
        if(filename == "xl"):
            html += "<ul>"
            for filename in listdir('resources/xl'):
                html += "<li>" + filename + "</li>"
            html += "</ul>"
    html += "</ul>"
    return html