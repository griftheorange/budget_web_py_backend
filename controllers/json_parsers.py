from controllers.data_handlers import DataHandlers as DH
import json

class JSONParsers:
    def fetch_data(filename, cols=None):
        format_set = {}
        format_set['data'] = DH.get_data(filename, cols).to_dict()
        format_set['line_data'] = DH.get_line_data(filename, cols)
        return format_set

    def fetch_line_data(filename, cols=None):
        return json.dumps(DH.get_line_data(filename, cols))

    
    def save_and_insert_file(file):
        return DH.save_and_insert_file(file).to_json()

