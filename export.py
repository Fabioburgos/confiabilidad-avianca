#Import the libraries
from re import search
import pandas as pd
from io import BytesIO
from flask import Flask, send_file

from search import Search

class Export:

    def new_dataframe(self, dataset_1,dataset_2):

        fleet = pd.read_csv('./in/fleet_table.csv', sep = ',')
        ata100_failures = pd.read_csv('./in/ATA100_fails.csv', sep = ',')

        search = Search()

        new_index_amos, new_list_report_amos = search.first_filter_amos(dataset_1)
        new_index_airman, new_list_report_airman = search.first_filter_airman(dataset_2)
        
        final_number_report = new_list_report_amos + new_list_report_airman

        columns_names = ['SISTEMA', 'AOC', 'RISK', 'FLEET', 'A/C', 'ATA4D', 'PIREPS/ WARNING/ FAULT MESSAGE', 'TASK / WO', 'ATA 100 Failures', 'RESPONSABLE', 'ISSUE DATE', 'DUE DATE', 'TRACING', 'OPEN DAY', 'NOTAS MCC', 'REMARKS']
        
        new_df = pd.DataFrame(dataset_1.iloc[new_index_amos], columns=columns_names)
        new_df_2 = new_df.append(dataset_2.iloc[new_index_airman]).reset_index()

        control_row_AC = ''
        control_row_ATA4D = ''
        control_index = 0

        new_df_2['AOC'] = new_df_2['AOC'].astype(str)
        new_df_2['FLEET'] = new_df_2['FLEET'].astype(str)
        new_df_2['ATA 100 Failures'] = new_df_2['ATA 100 Failures'].astype(str)
        new_df_2['ATA4D'] = new_df_2['ATA4D'].astype(str).replace('-', '', regex = True).str[:4].str.ljust(4,'0')
        new_df_2['TRACING'] = new_df_2['TRACING'].astype(str)
        new_df_2['OPEN DAY'] = new_df_2['OPEN DAY'].astype(str)

        for index, row in  new_df_2.iterrows():
            control_row_AC = row['A/C']
            control_row_ATA4D = row['ATA4D']
            control_index = index
            new_df_2['TRACING'].values[index] = '# reportes: {}'.format(final_number_report[index])

            for index_1, row_1 in fleet.iterrows():
                if (control_row_AC == row_1['A/C']):
                    new_df_2['AOC'].values[control_index] = row_1['AOC']
                    new_df_2['FLEET'].values[control_index] = row_1['FLEET']

            for index_1, row_1 in ata100_failures.iterrows():
                if (control_row_ATA4D == row_1['Ata 4D']):
                    new_df_2['ATA 100 Failures'].values[control_index] = row_1['Resumen']

        new_df_2 = new_df_2.drop_duplicates(subset = ['SISTEMA', 'A/C', 'PIREPS/ WARNING/ FAULT MESSAGE']).reset_index()

        for index, row in new_df_2.iterrows():
            #Check this information, ask if the correct column is Open day or Due date; check cell name (K or L), all depends on if we eliminate index row or not.
            new_df_2['OPEN DAY'].values[index] = '=TODAY()-K{}'.format(index+2)

        new_df_2 = new_df_2.drop(['index', 'level_0'], axis = 1)


        # #Name of the excel file
        # new_excel = pd.ExcelWriter(path_excel)

        output = BytesIO()

        with pd.ExcelWriter(output) as writer:
            new_df_2.to_excel(writer, sheet_name="Sheet1", index = False)
        
        output.seek(0)

        return send_file(output, attachment_filename="realibility.xlsx", as_attachment=True)

        # #Write DataFrame to excel
        # new_df_2.to_excel(new_excel, index = False)
        # new_excel.save()

