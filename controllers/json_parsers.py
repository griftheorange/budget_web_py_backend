from controllers.data_handlers import DataHandlers as DH
from constants import *
import json

# Router calls go to data_handlers from here IF a json object
# is needed for return. Done this way to separate dataframe manip from json returns
class JSONParsers:
    # Gets full table data and formatted line graph data from data handler
    # Packages both sets into relevant keys, return json object
    def fetch_data(filename):
        # Some columns need formatting to comma-separated 2-decimal dollar values
        columns_to_decimalize = ['Cost', 'Checking', 'Savings', 'Total', 'Total Income']
        format_set = {}
        table_data = DH.get_data(filename).to_dict()
        
        # Maps all values in Date to an StrfTime conversion
        table_data['Date'] = {k: v.strftime("%m/%d/%Y") for k,v in table_data['Date'].items()}
        
        # Maps all values in each of the decimalize columns to proper format
        for column in columns_to_decimalize:
            table_data[column] = {k: ("-${:,.2f}".format(v*-1) if v < 0 else "${:,.2f}".format(v)) for k,v in table_data[column].items()} 
        
        # Gets processed Line Data and places both in appropriate keys, returning dictionary
        format_set['table_data'] = table_data
        format_set['line_data'] = DH.get_line_data(filename, ColumnSets.LINE)
        format_set['spendings_pie_data'] = DH.get_pie_data(filename, Categories.SPENDINGS, ColumnSets.PIE)
        format_set['income_pie_data'] = DH.get_pie_data(filename, Categories.INCOME, ColumnSets.PIE)
        
        format_set['categories'] = Categories.GRIFFIN
        format_set['columns'] = ColumnSets.COLUMN_LIST
        return format_set

    # Fetches and returns only JSON of formatted line data
    # Not currently used
    def fetch_line_data(filename, cols=None):
        return json.dumps(DH.get_line_data(filename, cols))

    def patch_data(body):
        if((body['column'] in ColumnSets.COLUMN_LIST) and (body['category'] in Categories.GRIFFIN)):
            if(DH.update_cell(body)):
                return {
                    'status':'Success',
                    'body':body
                }
            return {'status':'Error'}
        return {'status':'Error'}
    
    def patch_new_entry(body):
        if(body['th'] and body['date'] and body['cost']):
            if(DH.add_entry(body)):
                return {
                    'status':'Success',
                    'body':body
                }
            return {'status':'Error'}
        return {'status':'Error'}
