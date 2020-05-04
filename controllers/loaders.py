import pandas as pd

#This class handles all file saving and file loading into pandas DFs
class Loaders:
    # below three methods load files of different types, could stand for refactoring
    def load_excel_file(filename, cols=None):
        if(cols == None):
            df = pd.read_excel("resources/xl/%s.xlsx"%filename, parse_dates=['Date'])
        else:
            df = pd.read_excel("resources/xl/%s.xlsx"%filename, usecols=cols, parse_dates=['Date'])
        
        df.filename = filename
        return df

    def load_pickle_file(filename, cols=None):
        if(cols == None):
            df = pd.read_pickle("resources/%s.p"%filename)
        else:
            df = pd.read_pickle("resources/%s.p"%filename)[cols]
        
        df.filename = filename
        return df

    def load_csv_file(filename, cols=None):
        if(cols == None):
            df = pd.read_csv("resources/csv/%s.csv"%filename)
        else:
            df = pd.read_csv("resources/csv/%s.csv"%filename, usecols=cols)
        
        df.filename = filename
        return df

    # below method recieves a file as a flask.FileStorage object
    # saves the file in resources directory dependant on file type
    # reads file at new address into DF and returns DF
    def save_and_load_file(file):
        df = None
        if("csv" in file.content_type):
            address = "resources/csv/%s"%(file.filename.replace(" ","_"))
            file.save(address)
            df = pd.read_csv(address)
        elif("officedocument" in file.content_type):
            address = "resources/xl/%s"%(file.filename.replace(" ","_"))
            file.save(address)
            df = pd.read_excel(address)
        return df