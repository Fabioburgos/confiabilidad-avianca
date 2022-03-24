#Import libraries
from optparse import Values
from iamodel import IAmodel

import pandas as pd
import numpy as np

class Search:

    def dif_dates(self, date_1, date_2):

        #Calculates the difference between two dates
        difference = date_2 - date_1

        #Converts the differences in terms of days
        # days_dif = (difference / np.timedelta64(1, 'D'))
        return (difference)

    #First filter issued by date, for Amos W/O with 30 days or less, may represent alert.
    def first_filter_amos(self, dataset):

        iamodel = IAmodel()

        list_report_index = []
        list_number_reports = []
        control_date  = False
        control_ac = False
        length_j = dataset.shape[0]
        index_i = 0
        control_report = 0
        control_text = 0
        controldate = 0
        controlac = ''
        controlreport = ''

        for index_1, row_1 in dataset.iterrows():

            index_j = index_1 + 1
            controldate = row_1['ISSUE DATE']
            controlac = row_1['A/C']
            controlreport = row_1['PIREPS/ WARNING/ FAULT MESSAGE']
            index_i = index_1

            while index_j < length_j:

                #control_date = controldate - dataset['ISSUE DATE'].values[index_j]
                control_ac = dataset['A/C'].values[index_i] == dataset['A/C'].values[index_j]
                
                if (control_ac): #and (control_date.days != 0):
                    control_text = iamodel.report_comparation(controlreport, dataset['PIREPS/ WARNING/ FAULT MESSAGE'].values[index_j])
                
                    if control_text >= 60:
                        control_report += 1

                index_j += 1

            if (control_report >= 3):
                list_report_index.append(index_i)
                list_number_reports.append(control_report)

            control_report = 0

        print('Terminamos Amos')
        return list_report_index, list_number_reports

    #First filter issued by date, may represent alert.
    def first_filter_airman(self, dataset):

        iamodel = IAmodel()

        list_report_index = []
        list_number_reports = []
        control_date  = False
        control_ac = False
        control_at = False
        length_j = dataset.shape[0]
        index_i = 0
        control_report = 0
        control_text = 0
        controldate = 0
        controlac = ''
        controlata = ''
        controlreport = ''

        for index_1, row_1 in dataset.iterrows():

            index_j = index_1 + 1
            controldate = row_1['ISSUE DATE']
            controlac = row_1['A/C']
            controlata = row_1['ATA4D']
            controlreport = row_1['PIREPS/ WARNING/ FAULT MESSAGE']
            index_i = index_1

            while index_j < length_j:

                #control_date = controldate - dataset['ISSUE DATE'].values[index_j]
                control_ac = dataset['A/C'].values[index_i] == dataset['A/C'].values[index_j]
                control_ata = dataset['ATA4D'].values[index_i] == dataset['ATA4D'].values[index_j]
                
                if (control_ac) and (controlata): #and (control_date.days != 0):
                    control_text = iamodel.report_comparation(controlreport, dataset['PIREPS/ WARNING/ FAULT MESSAGE'].values[index_j])
                
                    if control_text >= 90:
                        control_report += 1

                index_j += 1

            if (control_report >= 3):
                list_report_index.append(index_i)
                list_number_reports.append(control_report)

            control_report = 0

        print('Terminamos Airman')
        return list_report_index, list_number_reports