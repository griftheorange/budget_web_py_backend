from io import StringIO
from os import listdir
import shelve

from controllers.loaders import Loaders
from constants import *
import pandas as pd
import numpy as np

#Data Handlers Manipulates Dataframes and DataStructures for return/formatting
#Can call to the Loaders class for saving files and loading them into dataframes
class DataHandlers:

    # Serializer for resources directory
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
            

    # returns a default dataframe of the table data
    def get_data(cols=None):
        df = Loaders.load_data(cols)
        return df


    # returns an array of two key dictionary -> header and data
    # the data key points to an array of dictionaries with x,y keys pointing to coordinates for all data values of that series
    def get_line_data(cols=None):
        # Loads File from memory into df, initializes datasets and series ('Columns')
        df = Loaders.load_data(cols)
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


    # Returns a dictionary with two keys, data and label, pointing to arrays
    # Arrays hold data values and labels IN MATCHING ORDER for frontend interpretation
    def get_pie_data(cats, cols=None):
        df = Loaders.load_data(cols)
        df = df.groupby(['Type']).sum()
        # Below adjustments are personal, due to errors in my data, remove if you use
        df.at['INCOME', 'Cost'] += 10800
        df.at['TAX', 'Cost'] -= 5703.06
        df.at['UNTRACKED', 'Cost'] -= 3200
        # Sets framework, iterates through aggregate table and fills matching values
        # into arrays in order
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


    # Updates cell with new value. Overwrites pickle
    def update_cell(body):
        df = Loaders.load_data()
        df.at[int(body['index']), body['column']] = body['category']
        df.to_pickle(Routes.STORAGE_ADDRESS)
        return df.to_dict()
    
    # Adds a new Entry from submitted data
    def add_entry(body):
        # Below block loads in data.p, and initializes values of new row in a dictionary
        data = Loaders.load_data()
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
        # Coverts new_dataframe dict to dataframe
        new_dataframe = pd.DataFrame.from_dict(new_dataframe)
        # Concats new row to old dataframe
        data = pd.concat([data, new_dataframe])
        data.sort_values(by=['Date', 'Transaction History', 'Cost'], inplace=True)
        data.reset_index(drop=True, inplace=True)
        # Locates earliest index that Checking, Savings, Total etc will need recalc
        old_tail = data.shape[0]
        for index, row in data.iterrows():
            if(row['Date'] == min_date_in_new):
                old_tail = index
                break
        # Recalcs values, overwrites pickle, returns success
        DataHandlers.recalc_check_sav_tot_from(data, old_tail)
        data.to_pickle(Routes.STORAGE_ADDRESS)
        return True
    
    def delete_entry(body):
        df = Loaders.load_data()
        index = int(body['index'])
        try:
            df.drop(index, inplace=True)
        except KeyError:
            print("This key was out of bounds")
            return False
        else:
            df.reset_index(drop=True, inplace=True)
            DataHandlers.recalc_check_sav_tot_from(df, index-1)
            df.to_pickle(Routes.STORAGE_ADDRESS)
            return True


    # Loads dataframe and writes it as file in relevant directory based on submitted filename
    def save_backup(body):
        df = Loaders.load_data()
        tag = body['filetag']
        if(tag == 'p'):
            df.to_pickle(Routes.PICKLE+body['filename'])
            return True
        elif(tag == 'csv'):
            df.to_csv(Routes.CSV+body['filename'])
            return True
        elif(tag == 'xlsx'):
            df.to_excel(Routes.XL+body['filename'])
            return True
        else:
            return False
    
    # Very similar to save backup, but instead of saving, exports to frontend file of type dependant on submitted filename
    def export_file(body):
        df = Loaders.load_data()
        tag = body['filetag']
        if(tag == 'p'):
            address = Routes.EXPORTS+body['filename']
            df.to_pickle(address)
            return address
        elif(tag == 'csv'):
            address = Routes.EXPORTS+body['filename']
            df.to_csv(address)
            return address
        elif(tag == 'xlsx'):
            address = Routes.EXPORTS+body['filename']
            df.to_excel(address)
            return address
        else:
            return ""
        
    # Loads in submitted file, overwrites data.p with file data to reset
    def reset_from_backup(body):
        tag = body['filetag']
        if(tag == 'p'):
            df = Loaders.load_pickle_file(body['filename'])
            df.to_pickle(Routes.STORAGE_ADDRESS)
            return True
        elif(tag == 'csv'):
            df = Loaders.load_csv_file(body['filename'])
            df.to_pickle(Routes.STORAGE_ADDRESS)
            return True
        elif(tag == 'xlsx'):
            df = Loaders.load_excel_file(body['filename'])
            df.to_pickle(Routes.STORAGE_ADDRESS)
            return True
        else:
            return False

    def initialize_table(file):
        uploaded_file = Loaders.save_and_load_file(file)
        columns = uploaded_file.columns.tolist()
        for header in ColumnSets.COLUMN_LIST:
            if not header in uploaded_file.columns:
                return False
        uploaded_file.sort_values(by=['Date', 'Transaction History', 'Cost'], inplace=True)
        uploaded_file.reset_index(drop=True, inplace=True)
        uploaded_file.to_pickle(Routes.STORAGE_ADDRESS)
        return True

    # Saves a file sent back and inserts the data into the dataset
    def save_and_insert_file(file, card_type):
        preferences = shelve.open('resources/preferences')
        print(preferences)
        preferences.close()

        # Load in uploaded file and current data as DFs
        # Old tail is default index of earliest value to be updated (For updating derived values: Checking, Savings, Total, Total Inc)
        uploaded_file = Loaders.save_and_load_file(file)
        data = Loaders.load_data()
        old_tail = data.shape[0]

        # Sets framework to build a dataframe out of new data
        # Needed to map columns in uploaded CSVs to my data columns
        new_dataframe = DataHandlers.construct_new_dataframe_dict(uploaded_file, card_type)        
        min_date_in_new = min(new_dataframe['Date'])

        # Converts dict to DF, then concats to my data, and sorts them by date primarily, reseting index values
        new_dataframe = pd.DataFrame.from_dict(new_dataframe)
        data = pd.concat([data, new_dataframe])
        data.sort_values(by=['Date', 'Transaction History', 'Cost'], inplace=True)
        data.reset_index(drop=True, inplace=True)

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
            # Runs standard calc for all non-transfer rows
            if(not data.at[i, 'Type'] in ['TRANSFER']):
                data.at[i, 'Checking'] = data.at[i-1, 'Checking'] + data.at[i, 'Cost']
                data.at[i, 'Savings'] = data.at[i-1, 'Savings']
                data.at[i, 'Total'] = data.at[i, 'Checking'] + data.at[i, 'Savings']
                if(data.at[i, 'Cost'] >= 0 and data.at[i, 'Type'] != "TRANSFER"):
                    data.at[i, 'Total Income'] = data.at[i-1, 'Total Income'] + data.at[i, 'Cost']
                else:
                    data.at[i, 'Total Income'] = data.at[i-1, 'Total Income']
            # Below transforms the TRANSFER rows, which uniquely need to increment Cost AND Savings
            # Total Income NEVER incremented on TRANSFERS
            else:
                data.at[i, 'Checking'] = data.at[i-1, 'Checking'] + data.at[i, 'Cost']
                data.at[i, 'Savings'] = data.at[i-1, 'Savings'] - data.at[i, 'Cost']
                data.at[i, 'Total'] = data.at[i, 'Checking'] + data.at[i, 'Savings']
                data.at[i, 'Total Income'] = data.at[i-1, 'Total Income']
