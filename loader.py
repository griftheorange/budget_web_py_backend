import pandas as pd

def load_excel_file():
    df = pd.read_excel("resources/data.xlsx", parse_dates=['Date'])
    df.filename = "data"
    return df 