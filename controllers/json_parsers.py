from controllers.data_handlers import DataHandlers as DH
import json

# Router calls go to data_handlers from here IF a json object
# is needed for return. Done this way to separate dataframe manip from json returns
class JSONParsers:
    # Gets full table data and formatted line graph data from data handler
    # Packages both sets into relevant keys, return json object
    def fetch_data(filename, cols=None):
        format_set = {}
        format_set['data'] = DH.get_data(filename).to_dict()
        format_set['line_data'] = DH.get_line_data(filename, cols)
        return format_set

    # Fetches and returns only JSON of formatted line data
    # Not currently used
    def fetch_line_data(filename, cols=None):
        return json.dumps(DH.get_line_data(filename, cols))

