import pandas as pd


def load_excel_file(filename, cols=None):
    if(cols == None):
        df = pd.read_excel("resources/%s.xlsx"%filename, parse_dates=['Date'])
    else:
        df = pd.read_excel("resources/%s.xlsx"%filename, usecols=cols, parse_dates=['Date'])
    
    df.filename = "data"
    return df

def load_pickle_file(filename, cols=None):
    if(cols == None):
        df = pd.read_pickle("resources/%s.p"%filename)
    else:
        df = pd.read_pickle("resources/%s.p"%filename)[cols]
    
    df.filename = "data"
    return df