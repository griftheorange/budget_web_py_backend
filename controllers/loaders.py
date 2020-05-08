import pandas as pd
import numpy as np
import shelve
from constants import Routes

#This class handles all file saving and file loading into pandas DFs
class Loaders:
    # below four methods load files of different types
    def load_data(cols=None):
        if(cols == None):
            df = pd.read_pickle(Routes.STORAGE_ADDRESS)
        else:
            df =pd.read_pickle(Routes.STORAGE_ADDRESS)[cols]
        return df
    
    def load_excel_file(filename, cols=None):
        if(cols == None):
            df = pd.read_excel(Routes.XL+"%s"%filename, parse_dates=['Date'])
        else:
            df = pd.read_excel(Routes.XL+"%s"%filename, usecols=cols, parse_dates=['Date'])
        return df

    def load_pickle_file(filename, cols=None):
        if(cols == None):
            df = pd.read_pickle(Routes.PICKLE+"%s"%filename)
        else:
            df = pd.read_pickle(Routes.PICKLE+"%s"%filename)[cols]
        return df

    def load_csv_file(filename, cols=None):
        if(cols == None):
            df = pd.read_csv(Routes.CSV+"%s"%filename)
        else:
            df = pd.read_csv(Routes.CSV+"%s"%filename, usecols=cols)
        return df

    # below method recieves a file as a flask.FileStorage object
    # saves the file in resources directory dependant on file type
    # reads file at new address into DF and returns DF
    def save_and_load_file(file):
        df = None
        if("csv" in file.content_type):
            address = Routes.CSV+"%s"%(file.filename.replace(" ","_"))
            file.save(address)
            df = pd.read_csv(address)
        elif("officedocument" in file.content_type):
            address = Routes.XL+"%s"%(file.filename.replace(" ","_"))
            file.save(address)
            df = pd.read_excel(address)
            df.to_excel(address)
        else:
            address = Routes.PICKLE+"%s"%(file.filename.replace(" ","_"))
            file.save(address)
            df = pd.read_pickle(address)
        #TODO Add pickle format loader
        return df

    def initialize_files():
        data_framework = {
            'Transaction History':[],
            'Date':[],
            'Type':[],
            'Cost':[],
            'Checking':[],
            'Savings':[],
            'Total':[],
            'Total Income':[]
        }
        pd.DataFrame.from_dict(data_framework).to_pickle(Routes.STORAGE_ADDRESS)

        preferences = shelve.open(Routes.PREFERENCES_ADDRESS)
        try:
            preferences['user']
        except KeyError:
            preferences_framework = {
                'cards':{},
                'categories':{},
                'transfer_type':None,
                'correction_type':None
            }
            preferences['user'] = preferences_framework
        preferences.close()
        