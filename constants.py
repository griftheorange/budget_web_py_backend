# Column Collections from my dataset
# Used for selecting out columns for different operations
class ColumnSets:
    COLUMN_LIST = ['Transaction History', 'Date', 'Type', 'Cost', 'Checking', 'Savings', 'Total', 'Total Income']
    MONETARY = ['Cost', 'Checking', 'Savings', 'Total', 'Total Income']
    LINE = ['Transaction History', 'Date', 'Cost', 'Checking', 'Savings', 'Total', 'Total Income']
    PIE= ['Type', 'Cost']

# Collections of categories, primarily categories from the 'Type' column
# Also includes FILE_TAGS, listing acceptable file tags for export, save etc.
class Categories:
    GRIFFIN = ['BUSINESS','Correction','DINING','ENTERTAINMENT',
               'GAS','GROCERY','HEALTHCARE','INCOME','RENT',
               'SCHOOL','SHOPPING','TAX','TRANSFER','TRAVEL',
               'UNTRACKED','UTILITIES']
    SPENDINGS = ['BUSINESS','DINING','ENTERTAINMENT',
               'GAS','GROCERY','HEALTHCARE','RENT',
               'SCHOOL','SHOPPING','TRAVEL','UTILITIES']
    INCOME = ['BUSINESS','DINING','ENTERTAINMENT',
               'GAS','GROCERY','HEALTHCARE','INCOME','RENT',
               'SCHOOL','SHOPPING','TAX','TRAVEL',
               'UNTRACKED','UTILITIES']
    FILE_TAGS = ['p','csv','xlsx']
    
# Stores routes for saving and loading files
# Typically saving is done straight from data_handlers, and file loading done in loaders
class Routes:
    STORAGE_ADDRESS = 'resources/data.p'
    PICKLE = 'resources/pickle/'
    CSV = 'resources/csv/'
    XL = 'resources/xl/'
    EXPORTS = 'resources/exports/'
