from controllers.data_handlers import *
import json

def fetch_line_data(filename, cols=None):
    return json.dumps(get_line_data(filename, cols))

def fetch_data(filename, cols=None):
    return get_data(filename, cols).to_json()

def fetch_print_csv():
    load_and_print_csv()