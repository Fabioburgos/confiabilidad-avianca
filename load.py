#Import neccesary modules to make the program work correctly
import numpy as np
import pandas as pd

#Import classes from other files
from utils import Utils

class Load:
    #Method to import and clean the data obtained from AMOS.
    def read_file_amos(self, path):
        utils = Utils()
        init_dataset = pd.read_csv(path, sep = ';')
        X_0 = init_dataset.drop(['No', 'Unnamed: 14', 'Unnamed: 15', 'Due-/C.-Date', 'Parts', 'Ref.', 'DD'], axis = 1)

        #For Amos csv, Issue-Date is the only datetime column able to convert to datetime64.
        X_1 = utils.convert_time_amos(X_0, 'Issue-Date')

        #W/O correspond to Work Order, that cell cannot be empty, so any row without W/O is eliminated
        X_2 = utils.drop_nan(X_1, 'W/O')

        #Convertion of W/O values from float to int in order to save memory.
        X_2['W/O'] = X_2['W/O'].astype('int')

        X_2['SISTEMA'] = 'Amos'

        #State change from Open and Closed to 1 and 0 (Open = 1, Closed = 0)
        X_3 = utils.state_change(X_2)

        #Sorting dataframe by column "Issue-Date" from older to newest.
        # X_4 = utils.sort_issue_date(X_3, 'Issue-Date')

        X_4 = utils.drop_type_not_pirep_amos(X_3)

        #Split Date to day, month and year columns
        X_5 = utils.split_date_columns(X_4, 'Issue-Date')

        #Only for Amos, select the first 100 characters from report in order to apply IA.
        X_5['Workorder-description and/or complaint'] = X_5['Workorder-description and/or complaint'].astype(str).str[:70]

        #Change columns names
        X_6 = X_5.rename({'A/C' : 'A/C', 
                        'W/O' : 'TASK / WO',
                        'Workorder-description and/or complaint' : 'PIREPS/ WARNING/ FAULT MESSAGE',
                        'Iss' : 'RESPONSABLE',
                        'ATA' : 'ATA4D',
                        'Issue-Date' : 'ISSUE DATE'}, axis = 1)

        return X_6

    #Method to import and clean the data obtained from Airman.
    def read_file_airman(self, path):
        utils = Utils()
        init_dataset = pd.read_csv(path, sep = ';', skiprows = 18)

        X_0 = init_dataset.drop(['Leg', 'Fault Tracking', 'Flight Number', 'Flight phase', 'Transmission Date', 'Priority', 'Correlated', 'Rate', 'Airline rate', 'Airbus rate', 'Report', 'Work', 'Note', 'Source'], axis = 1)

        #For Amos csv, Issue-Date is the only datetime column able to convert to datetime64.
        X_1 = utils.convert_time_airman(X_0, 'Date Time')

        #W/O correspond to Work Order, that cell cannot be empty, so any row without W/O is eliminated
        X_2 = utils.drop_nan(X_1, 'Date Time')

        X_2['SISTEMA'] = 'Airman'

        #Sorting dataframe by column "Issue-Date" from older to newest.
        X_3 = utils.sort_issue_date(X_2, 'Date Time')

        #Split Date to day, month and year columns
        X_4 = utils.split_date_columns(X_3, 'Date Time')

        #Format A/C Id to make it compatible with aircraft fleet database
        X_4['A/C ID'] = X_4['A/C ID'].astype(str).replace(['N', 'HK-', 'HC-'], '', regex = True)

        # #Format ATA column to make it compatible with ATA 100
        # X_5 = utils.split_ATA(X_4)
        # X_5['ATA'] = X_5['ATA'].astype(str).str[:4].str.ljust(4,'0')

        #Change columns names
        X_5 = X_4.rename({'A/C ID' : 'A/C', 
                        'Title' : 'PIREPS/ WARNING/ FAULT MESSAGE',
                        'ATA' : 'ATA4D',
                        'Date Time': 'ISSUE DATE'}, axis = 1)
        return X_5