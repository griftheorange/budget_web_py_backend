from controllers.data_handlers import DataHandlers as DH
from constants import *
import json

# Router calls go to data_handlers from here IF a json object
# is needed for return. Done this way to separate dataframe manip from json returns
class JSONParsers:

    # MAIN SERIALIZER FOR APP
    # Gets full table data and formatted line graph data from data handler
    # Packages both sets into relevant keys, return json object
    def fetch_data():
        # Some columns need formatting to comma-separated 2-decimal dollar values
        format_set = {}
        table_data = DH.get_data().to_dict()
        
        # Maps all values in Date to an StrfTime conversion
        table_data['Date'] = {k: v.strftime("%m/%d/%Y") for k,v in table_data['Date'].items()}
        
        # Maps all values in each of the decimalize columns to proper format
        for column in ColumnSets.MONETARY:
            table_data[column] = {k: ("-${:,.2f}".format(v*-1) if v < 0 else "${:,.2f}".format(v)) for k,v in table_data[column].items()} 
        
        # Gets processed Line Data and places both in appropriate keys, returning dictionary
        format_set['table_data'] = table_data
        format_set['line_data'] = DH.get_line_data(ColumnSets.LINE)
        format_set['spendings_pie_data'] = DH.get_pie_data(Categories.SPENDINGS, ColumnSets.PIE)
        format_set['income_pie_data'] = DH.get_pie_data(Categories.INCOME, ColumnSets.PIE)
        format_set['resources'] = DH.get_resources_filenames()
        format_set['cards'] = DH.get_card_list()
        
        format_set['categories'] = Categories.GRIFFIN
        format_set['columns'] = ColumnSets.COLUMN_LIST
        return format_set


    # Checks for valid values of column and category for editing
    # Currentl, only Type column is able to be edited ever
    def patch_data(body):
        if((body['column'] in ColumnSets.COLUMN_LIST) and (body['category'] in Categories.GRIFFIN)):
            success = DH.update_cell(body)
            if(success):
                return {
                    'status':'Success',
                    'body':body
                }
            return {'status':'Error'}
        return {'status':'Error'}
    
    def initialize_table(file):
        if(DH.initialize_table(file)):
            return {
                'status':'Success'
            }
        return {'status':'Error'}
    
    # Checks for presence of minimum required entries
    # Attempts to add new entries
    def patch_new_entry(body):
        if(body['th'] and body['date'] and body['cost']):
            if(DH.add_entry(body)):
                return {
                    'status':'Success',
                    'body':body
                }
            return {'status':'Error'}
        return {'status':'Error'}
    
    def delete_entry(body):
        if(body['index']):
            if(DH.delete_entry(body)):
                return {
                    'status':'Success',
                    'body':body
                }
            return {'status':'Error'}
        return {'status':'Error'}
    
    # Checks for valid file tags
    # Attempts to save current data with filename and format matching submitted
    def save_backup(body):
        if(body['filetag'] and body['filetag'] in Categories.FILE_TAGS):
            if(DH.save_backup(body)):
                return {
                    'status':'Success',
                    'body':body
                }
        return {'status':'Error'}
    
    # Checks for valid File tags 
    # Attempts to load File from backups based on filename and extension, then overwrites data.p
    def reset_from_backup(body):
        if(body['filetag'] and body['filetag'] in Categories.FILE_TAGS):
            if(DH.reset_from_backup(body)):
                return {
                    'status':'Success',
                    'body':body
                }
            return {'status':'Error'}
        return {'status':'Error'}