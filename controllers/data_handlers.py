from io import StringIO
from os import listdir

from controllers.loaders import Loaders
from constants import *
import pandas as pd

#Data Handlers Manipulates Dataframes and DataStructures for return/formatting
#Can call to the Loaders class for saving files and loading them into dataframes
class DataHandlers:

    def get_resources_filenames():
        resources = {
            'csv':[],
            'xl':[],
            'pickle':[]
        }
        for key in resources.keys():
            for filename in listdir('resources/'+key):
                resources[key].append(filename)
        return resources
            

    # returns a data frame of the loaded file
    def get_data(filename, cols=None):
        df = Loaders.load_pickle_file(filename, cols)
        return df

    # returns an array of two key dictionary -> header and data
    # the data key points to an array of dictionaries with x,y keys pointing to coordinates for all data values of that series
    def get_line_data(filename, cols=None):
        # Loads File from memory into df, initializes datasets and series ('Columns')
        df = Loaders.load_pickle_file(filename, cols)
        datasets = []
        series = df.columns
        series = series.delete(series.get_loc("Date"))
        series = series.delete(series.get_loc('Transaction History'))

        # Maps columns to objects, column head goes to header key
        # Data key will hold array of formatted data objects
        for i in range(0, len(series)):
            datasets.append({
                'header': series[i],
                'data': []
                })
        # Iterates through rows, then takes each column values out of the row
        # and inserts the necessary data into the corresponding dataset array
        for index, row in df.iterrows():
            count = 0
            for header in series:
                datasets[count]['data'].append({
                    'x': row["Date"].timestamp(),
                    'y': round(row[header], 2),
                    'name':row['Transaction History']
                })
                count += 1

        return datasets

    def get_pie_data(filename, cats, cols=None):
        df = Loaders.load_pickle_file(filename, cols)
        df = df.groupby(['Type']).sum()
        df.at['INCOME', 'Cost'] += 10800
        df.at['TAX', 'Cost'] -= 5703.06
        df.at['UNTRACKED', 'Cost'] -= 3200

        dataset = {
            'data':[],
            'labels':[]
        }
        for i in range(len(cats)):
            datum = df.at[cats[i], 'Cost']
            if(datum < 0):
                datum *= -1
            dataset['data'].append(round(datum, 2))
            dataset['labels'].append(cats[i])
        return dataset

    def update_cell(body):
        df = Loaders.load_pickle_file('data')
        df.at[int(body['index']), body['column']] = body['category']
        df.to_pickle(Routes.STORAGE_ADDRESS)
        return True
    
    def add_entry(body):
        data = Loaders.load_pickle_file('data')
        new_dataframe = {}
        new_dataframe['Transaction History'] = [body['th']]
        min_date_in_new = pd.Timestamp(body['date'])
        new_dataframe['Date'] = [min_date_in_new]
        if(body['type']):
            new_dataframe['Type'] = [body['type']]
        else:
            new_dataframe['Type'] = ['N/A']
        new_dataframe['Cost'] = [float(body['cost'])]
        new_dataframe['Checking'] = [0]
        new_dataframe['Savings'] = [0]
        new_dataframe['Total'] = [0]
        new_dataframe['Total Income'] = [0]
        new_dataframe = pd.DataFrame.from_dict(new_dataframe)
        data = pd.concat([data, new_dataframe]).sort_values(by=['Date', 'Type', 'Transaction History', 'Cost']).reset_index(drop=True)
        old_tail = data.shape[0]

        for index, row in data.iterrows():
            if(row['Date'] == min_date_in_new):
                old_tail = index
                break
        DataHandlers.recalc_check_sav_tot_from(data, old_tail)
        data.to_pickle(Routes.STORAGE_ADDRESS)
        return True
    
    def save_backup(body):
        df = Loaders.load_pickle_file('data')
        tag = body['filetag']
        if(tag == 'p'):
            df.to_pickle('resources/pickle/'+body['filename'])
            return True
        elif(tag == 'csv'):
            df.to_csv('resources/csv/'+body['filename'])
            return True
        elif(tag == 'xlsx'):
            df.to_excel('resources/xl/'+body['filename'])
            return True
        else:
            return False
        

    # Saves a file sent back and inserts the data into the dataset
    def save_and_insert_file(file, card_type):
        # Load in uploaded file and current data as DFs
        # Old tail is default index of earliest value to be updated (For updating derived values: Checking, Savings, Total, Total Inc)
        uploaded_file = Loaders.save_and_load_file(file)
        data = Loaders.load_pickle_file("data")
        old_tail = data.shape[0]

        # Sets framework to build a dataframe out of new data
        # Needed to map columns in uploaded CSVs to my data columns
        new_dataframe = DataHandlers.construct_new_dataframe_dict(uploaded_file, card_type)        
        min_date_in_new = min(new_dataframe['Date'])

        # Converts dict to DF, then concats to my data, and sorts them by date primarily, reseting index values
        new_dataframe = pd.DataFrame.from_dict(new_dataframe)
        data = pd.concat([data, new_dataframe]).sort_values(by=['Date', 'Type', 'Transaction History', 'Cost']).reset_index(drop=True)

        # Uses the minimum date in the new data defined above
        # Finds first index occurrence of lowest added date for the new data
        # This way, if data is added that is inserted BEFORE previous existing data,
        # the derived values (Check, Sav, Tot etc) will adjust properly
        # This does have the side-effect of overwriting sacvings transfers, but this can be accounted for later
        for index, row in data.iterrows():
            if(row['Date'] == min_date_in_new):
                old_tail = index
                break

        # Iterates and calculates column values for derived columns
        DataHandlers.recalc_check_sav_tot_from(data, old_tail)
        
        # Saves shiny new Data to pickle fiel
        data.to_pickle(Routes.STORAGE_ADDRESS)


    # Helper function for save_and_insert file
    # Constructs dict framework for new dataframe, and based on card type, parses the column values into the right slots
    # TODO Error catching
    def construct_new_dataframe_dict(file, card_type):
        new_dataframe = {}
        for column in ColumnSets.COLUMN_LIST:
            new_dataframe[column] = []
        # Iterate through uploaded data and insert datum where appropriate
        if(card_type == "TD"):
            for index, row in file.iterrows():
                if(row['Amount'] >= 0):
                    new_dataframe['Transaction History'].append(row['Merchant Name'])
                    new_dataframe['Date'].append(pd.Timestamp(row['Date']))
                    new_dataframe['Type'].append('N/A')
                    new_dataframe['Cost'].append(-1*row['Amount'])
                    new_dataframe['Checking'].append(0)
                    new_dataframe['Savings'].append(0)
                    new_dataframe['Total'].append(0)
                    new_dataframe['Total Income'].append(0)
        else:
            for index, row in file.iterrows():
                if(row['Amount'] >= 0):
                    new_dataframe['Transaction History'].append(row['Description'])
                    new_dataframe['Date'].append(pd.Timestamp(row['Trans. Date']))
                    new_dataframe['Type'].append('N/A')
                    new_dataframe['Cost'].append(-1*row['Amount'])
                    new_dataframe['Checking'].append(0)
                    new_dataframe['Savings'].append(0)
                    new_dataframe['Total'].append(0)
                    new_dataframe['Total Income'].append(0)
        return new_dataframe

    # Helper funciton for recalculating Checking, Saving, Total, Total Income Columns
    # Using start index, updates values in relavent rows until end of dataframe 
    # TRANSFER rows handle derived columns differently, this function should respond correctly to this behavior
    def recalc_check_sav_tot_from(data, start):
        end = data.shape[0]
        for i in range(start, end):
            if(not data.at[i, 'Type'] in ['TRANSFER']):
                data.at[i, 'Checking'] = data.at[i-1, 'Checking'] + data.at[i, 'Cost']
                data.at[i, 'Savings'] = data.at[i-1, 'Savings']
                data.at[i, 'Total'] = data.at[i, 'Checking'] + data.at[i, 'Savings']
                if(data.at[i, 'Cost'] >= 0 and data.at[i, 'Type'] != "TRANSFER"):
                    data.at[i, 'Total Income'] = data.at[i-1, 'Total Income'] + data.at[i, 'Cost']
                else:
                    data.at[i, 'Total Income'] = data.at[i-1, 'Total Income']
            else:
                data.at[i, 'Checking'] = data.at[i-1, 'Checking'] + data.at[i, 'Cost']
                data.at[i, 'Savings'] = data.at[i-1, 'Savings'] - data.at[i, 'Cost']
                data.at[i, 'Total'] = data.at[i, 'Checking'] + data.at[i, 'Savings']
                data.at[i, 'Total Income'] = data.at[i-1, 'Total Income']


    ####################################################
    # Below is for testing primarily
    
    def load_and_print_csv():
        df = Loaders.load_csv_file("transactions2")
        pd.set_option("display.max_columns",None)
        print(df)

    def reset_pickle():
        Loaders.load_excel_file('data').to_pickle(Routes.STORAGE_ADDRESS)
