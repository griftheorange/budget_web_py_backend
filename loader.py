import pandas as pd

def load_excel_file(cols=None):
    if(cols == None):
        df = pd.read_excel("resources/data.xlsx", parse_dates=['Date'])
    else:
        df = pd.read_excel("resources/data.xlsx", usecols=cols, parse_dates=['Date'])
    
    df.filename = "data"
    return df 