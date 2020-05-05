import pandas as pd
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
        #TODO Add pickle format loader
        return df