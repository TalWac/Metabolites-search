import pandas as pd
import json
import time
import fuzzymatcher

# r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/test_larger_list.xlsx'

# Load the parse HMDB file
# with open('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/serum_metabolites.json', 'r') as read_file:
#     data = json.load(read_file)

# If while istalling fuzzymatcer receive an error
# error: Microsoft Visual C++ 14.0 is required.
# Get it with "Build Tools for Visual Studio": https://visualstudio.microsoft.com/downloads/
# go to link https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat
# and download the first comment file "Visual C++ 2015 Build Tools. " by  Lalit Kumar B Aug 29 '18
#

with open('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Output/saliva_metabolites.json', 'r') as read_file:
    data = json.load(read_file)

df_excel = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/test_larger_list.xlsx')

def joindata(jsonpathin, excelpathin, excelpathout):
    '''
    The function takes 2 files and merge them by columns
    :param jsonpathin: path to JSON file parsed XML file from HMDB
    :param excelpathin: path to Excel file the output of LC-MS - Should be of the form r'path'
    :param excelpathout: path to output Excel after the merge.
    :return: The columns of the Excel file with added column  (diseas name) from the JSON
    '''

    # Load the parse HMDB file
    with open(jsonpathin, 'r') as read_file:
        data = json.load(read_file)

    # create a data frame from the list of dictionaries
    # df_hmdb = pd.DataFrame(data,  columns=['accession', 'name', 'chemical_formula', 'inchikey', 'disease_name' ])
    df_hmdb = pd.DataFrame(data)
    df_hmdb.drop(['description', 'synonyms', 'kegg_id', 'meta_cyc_id', 'pathway_name'], axis=1)
    # Load the Excel file -
    # df_excel = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites.xlsx', sheet_name='UP')
    # df_excel = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites.xlsx', sheet_name='DOWN')

    # load the Excel file
    df_excel = pd.read_excel(excelpathin)

    # df_excel = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/CD_10metabolites.xlsx')

    # merge by inchikey
    joindata_by_inchikey = pd.merge(left=df_excel, right=df_hmdb, how='inner', left_on='InChIKey', right_on='inchikey')

    # reduce the rows to those we DID find a match by inchkey in bothe data sets
    df_hmdb_reduce_byinchik= df_hmdb.loc[~df_hmdb['inchikey'].isin(df_excel['InChIKey'])]
    df_excel_reduce_byinchik = df_excel.loc[~df_excel['InChIKey'].isin(joindata_by_inchikey['InChIKey'])]


    start_time = time.time()
    # joindata_by_name = fuzzymatcher.fuzzy_left_join(df_excel, df_hmdb, left_on="Name", right_on="name")
    joindata_by_name = fuzzymatcher.fuzzy_left_join(df_excel_reduce_byinchik, df_hmdb_reduce_byinchik, left_on="Name", right_on="name")

    # selecting threshold  best_match_score>0.25 maybe adjustments needed
    joindata_by_name = joindata_by_name[joindata_by_name['best_match_score'] > 0.25]
    # Drop columns the
    joindata_by_name.drop(['best_match_score', '__id_left', '__id_right'], axis=1, inplace=True)
    print("--- %s seconds --f-" % (time.time() - start_time))

    # reduce the rows to those we DID find a match by inchkey in and by name both data sets
    df_hmdb_reduce_byname = df_hmdb_reduce_byinchik.loc[~df_hmdb_reduce_byinchik['name'].isin(joindata_by_name['name'])]
    df_excel_reduce_byname = df_excel_reduce_byinchik.loc[~df_excel_reduce_byinchik['Name'].isin(joindata_by_name['Name'])]
    # remove spaces between letters on  'Formula' ( there is  a warning)
    df_excel_reduce_byname.loc[:, 'Formula'] = df_excel_reduce_byname['Formula'].str.replace(' ', '')

    joindata_by_CF = pd.merge(left=df_excel_reduce_byname, right=df_hmdb_reduce_byname, how='inner', left_on='Formula', right_on='chemical_formula')

    #  append to 2 merge datasets to 1
    joindata_by_inchikey.append(joindata_by_name.append(joindata_by_CF))
    # return joindata_by_name

    # with open('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/differential_metabolites.xlsx', 'w') as fout:
    #     json.dump(saliva_metabolites, fout, indent=4)

    # writer = pd.ExcelWriter('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/test_larger_listW disease name.xlsx',
    #                         engine='xlsxwriter')

    # Export the merge data to an Excel file
    writer = pd.ExcelWriter(excelpathout, engine='xlsxwriter')

    joindata_by_inchikey.to_excel(writer,  header=True)
    writer.save()
    writer.close()

# joindata = pd.merge(left=df_excel, right=df_hmdb, how='left', left_on='ID', right_on='accession')


writer = pd.ExcelWriter('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/joindata_by_name.xlsx', engine='xlsxwriter')

joindata_by_name.to_excel(writer,  header=True)
df.loc[:, 'foo':'sat']
df_hmdb = pd.DataFrame(data)
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


