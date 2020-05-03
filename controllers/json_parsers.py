from controllers.data_handlers import DataHandlers as DH
import json

class JSONParsers:
    def fetch_line_data(filename, cols=None):
        return json.dumps(DH.get_line_data(filename, cols))

    def fetch_data(filename, cols=None):
        return DH.get_data(filename, cols).to_json()
    
    def save_and_insert_file(file):
        return DH.save_and_insert_file(file).to_json()

