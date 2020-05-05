class ColumnSets:
    COLUMN_LIST = ['Transaction History', 'Date', 'Type', 'Cost', 'Checking', 'Savings', 'Total', 'Total Income']
    LINE = ['Transaction History', 'Date', 'Cost', 'Checking', 'Savings', 'Total', 'Total Income']
    PIE= ['Type', 'Cost']

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
    

class Routes:
    DATA = 'data'
    STORAGE_ADDRESS = 'resources/data.p'
    PICKLE = 'resources/pickle/'
    CSV = 'resources/csv/'
    XL = 'resources/xl/'
    EXPORTS = 'resources/exports/'
