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
#############################################################################################

#default route to check if server is running properly
@app.route('/')
def hello_world():
    return "<h1 style='color:blue;'>Hello World!</h1>"

#Index for all files in resource directory, may be needed by frontend in future
@app.route('/data', methods=['GET'])
def data_index():
    print(listdir('resources'))
    html = get_filenames()
    return html

#Getter for bundled data, packages data => json and formatted line data => json into two keys, "data" and "line_data"
@app.route('/data/<filename>', methods=["GET"])
def data(filename):
    cols = ColumnSets.BUDGET_ALL
    return JSON.fetch_data(filename, cols=cols)

#saves file to proper directory loads in data, updates data.p and returns json
#inserts to data.p and returns success or failure
@app.route('/data', methods=["POST"])
def post_data():
    file = request.files['file']
    card_type = request.args['cardType']
    if(file):
        DH.save_and_insert_file(file, card_type)
        return "Success"
    return "Failed"

@app.route('/update_cell', methods=["PATCH"])
def update_cell():
    body = request.json
    if((body['column'] in ColumnSets.COLUMN_LIST) and (body['category'] in Categories.GRIFFIN)):
        if(DH.update_cell(body)):
            return {
                'status':'Success',
                'body':body
            }
        return {'status':'Error'}
    return {'status':'Error'}
    

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
    return "Success"

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