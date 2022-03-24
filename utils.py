#Import neccesary modules to make the program work correctly
import pandas as pd

class Utils:
    #Method to select columns with an specific value
    def select_columns(self, dataset, column_name, value):
        df = dataset.loc[dataset[column_name] == value]
        return df

    #Method to convert values into datetime 64 bits, the format is exclusevly to convert Amos data.
    def convert_time_amos(self, dataset, column_name):
        dataset[column_name] = pd.to_datetime(dataset[column_name], format = '%d.%b.%Y')
        return dataset

    #Method to convert values into datetime 64 bits, the format is exclusevly to convert Airman data.
    def convert_time_airman(self, dataset, column_name):
        dataset[column_name] = pd.to_datetime(dataset[column_name]).dt.normalize()
        return dataset

    #Method to erase columns not necessary in the analysis.
    def drop_nan(self, dataset, column_name):
        df = dataset.dropna(subset = [column_name])
        return df

    #Method to convert States Open and Closed into 0 and 1 (0 = Open, 1 = Closed) only for AMOS
    def state_change(self, dataset):
        wo_state = {
            'Open' : 1,
            'Closed' : 0
        }
        dataset.State = [wo_state[item] for item in dataset.State]
        return dataset

    #Method to sort the dataset by column
    def sort_issue_date(self, dataset, column_name):
        dataset_sorted = dataset.sort_values(by = column_name)
        return dataset_sorted

    #Method to erase all the rows differents to Pirep
    def drop_type_not_pirep_amos(self, dataset):
        dataset_sorted = dataset.drop(dataset[dataset['Type'] != 'P'].index)
        return dataset_sorted

    #Method to split columns to day, month and year
    def split_date_columns(self, dataset, column_name):
        dataset[column_name] = dataset[column_name].dt.date
        return dataset
