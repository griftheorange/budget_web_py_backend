from loaders import *
import pandas as pd

# returns a data frame of the loaded file
def get_data(filename, cols=None):
    df = load_pickle_file(filename, cols)
    return df

# returns an array of two key dictionaries -> header and data
# the data key points to an array of dictionaries with x,y keys pointing to coordinates for all data values of that series
def get_line_data(filename, cols=None):
    df = load_pickle_file(filename, cols)
    datasets = []
    series = df.columns
    series = series.delete(series.get_loc("Date"))
    for i in range(0, len(series)):
        datasets.append({
            'header': series[i],
            'data': []
            })
    for index, row in df.iterrows():
        count = 0
        for header in series:
            datasets[count]['data'].append({
                'x': row["Date"].timestamp(),
                'y': row[header]
            })
            count += 1

    return datasets
