from io import StringIO
from controllers.loaders import Loaders
import pandas as pd

#Data Handlers Manipulates Dataframes and DataStructures for return/formatting
#Can call to the Loaders class for saving files and loading them into dataframes
class DataHandlers:
    # returns a data frame of the loaded file
    def get_data(filename, cols=None):
        df = Loaders.load_pickle_file(filename, cols)
        return df

    # returns an array of two key dictionaries -> header and data
    # the data key points to an array of dictionaries with x,y keys pointing to coordinates for all data values of that series
    def get_line_data(filename, cols=None):
        df = Loaders.load_pickle_file(filename, cols)
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

    #Below is for testing
    def save_and_print_file(file):
        df = Loaders.save_and_load_file(file)
        print(df)

    def load_and_print_csv():
        df = Loaders.load_csv_file("transactions2")
        pd.set_option("display.max_columns",None)
        print(df)