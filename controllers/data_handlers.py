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

    #Saves a file sent back and inserts the data into the dataset
    def save_and_insert_file(file):
        #load in uploaded file and current data as DFs
        uploaded_file = Loaders.save_and_load_file(file)
        data = Loaders.load_pickle_file("data")
        old_tail = data.shape[0]

        #Sets framework for data map
        new_dataframe = {
            'Transaction History':[],
            'Date':[],
            'Type':[],
            'Cost':[],
            'Checking':[],
            'Savings':[],
            'Total':[],
            'Total Income':[]
        }
        #iterate through uploaded data and insert datum where appropriate
        for index, row in uploaded_file.iterrows():
            if(row['Amount'] >= 0):
                new_dataframe['Transaction History'].append(row['Merchant Category Description'])
                new_dataframe['Date'].append(pd.Timestamp(row['Date']))
                new_dataframe['Type'].append('N/A')
                new_dataframe['Cost'].append(-1*row['Amount'])
                new_dataframe['Checking'].append(0)
                new_dataframe['Savings'].append(0)
                new_dataframe['Total'].append(0)
                new_dataframe['Total Income'].append(0)
        min_date_in_new = min(new_dataframe['Date'])

        #converts dict to DF, then concats to my data, and sorts by date, reseting index values
        new_dataframe = pd.DataFrame.from_dict(new_dataframe).sort_values(by="Date")
        data = pd.concat([data, new_dataframe]).sort_values(by=['Date', 'Type']).reset_index(drop=True)
        new_tail = data.shape[0]

        #finds first index occurrence of lowest added date for 
        for index, row in data.iterrows():
            if(row['Date'] == min_date_in_new):
                old_tail = index
                break

        #iterates and calculates column values for derived columns
        DataHandlers.recalc_check_sav_tot_from(data, old_tail, new_tail)
        data.to_pickle('resources/data.p')
        return data

    def recalc_check_sav_tot_from(data, start, end):
        for i in range(start, end):
            data.at[i, 'Checking'] = data.at[i-1, 'Checking'] + data.at[i, 'Cost']
            data.at[i, 'Savings'] = data.at[i-1, 'Savings']
            data.at[i, 'Total'] = data.at[i, 'Checking'] + data.at[i, 'Savings']
            if(data.at[i, 'Cost'] >= 0):
                data.at[i, 'Total Income'] = data.at[i-1, 'Total Income'] + data.at[i, 'Cost']
            else:
                data.at[i, 'Total Income'] = data.at[i-1, 'Total Income']

    def load_and_print_csv():
        df = Loaders.load_csv_file("transactions2")
        pd.set_option("display.max_columns",None)
        print(df)

    def reset_pickle():
        Loaders.load_excel_file('xl/data').to_pickle('resources/data.p')