import pandas as pd
import json
import openpyxl

import saliva_metabolites
from openpyxl import Workbook

# Load the parse HMDB file
with open('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/hmdb_metabolites.json', 'r') as read_file:
    data = json.load(read_file)

# create a data frame from the list of dictionaries
df_hmdb = pd.DataFrame(data,  columns=['accession', 'name', 'chemical_formula', 'inchikey', 'disease_name'])

# Load the Excel file -
# df_excel = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites.xlsx', sheet_name='UP')
# df_excel = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites.xlsx', sheet_name='DOWN')


# df_excel = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/test_larger_list.xlsx')


# joindata = pd.merge(left=df_excel, right=df_hmdb, how='left', left_on='ID', right_on='accession')



joindata_by_inchikey = pd.merge(left=df_excel, right=df_hmdb, how='inner', left_on='InChIKey', right_on='inchikey')



joindata_by_accessionD.to_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolitesW disease.xlsx', sheet_name='DOWN', header=True)
joindata_by_accessionU.to_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolitesW disease.xlsx', sheet_name='UP', header=True)







pd.set_option('display.max_columns', 7)
pd.set_option('display.max_colwidth', -1)
pd.options.display.max_rows
df_excel.loc[joindata['InChIKey'].isin()]

df_excel['InChIKey']
df_hmdb.loc[df_hmdb['accession'] == 'HMDB0000696']
df_excel.loc[df_excel['ID'] == 'HMDB0000696']
df_hmdb.loc[~df_hmdb['inchikey'].isin(df_excel['InChIKey'])]


##########################################
# df_exceD = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites_ID_fixed.xlsx', sheet_name='DOWN')
# df_excelU = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites_ID_fixed.xlsx', sheet_name='UP')

# joindata_by_accessionD = pd.merge(left=df_exceD, right=df_hmdb, how='inner', left_on='IDFIXED', right_on='accession')
# joindata_by_accessionU = pd.merge(left=df_excelU, right=df_hmdb, how='inner', left_on='IDFIXED', right_on='accession')
#
#
# writer = pd.ExcelWriter('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolitesW disease.xlsx', engine='xlsxwriter')
#
# joindata_by_accessionD.to_excel(writer, sheet_name='DOWN', header=True)
# joindata_by_accessionU.to_excel(writer, sheet_name='UP', header=True)
# writer.save()
# writer.close()
##########################################


# wb1 = openpyxl.load_workbook('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites.xlsx')
# df2 = pd.DataFrame(wb1['UP'].values)
# wb1.append(["Name", "ID"])
# print (wb1.sheetnames)

