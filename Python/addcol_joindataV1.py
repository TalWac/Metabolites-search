import pubchempy as pcp
from rdkit import Chem
import numpy as np
import pandas as pd
import json
import time
import fuzzymatcher

def addcols_joindata(excelpathin, jsonpathin, excelpathout):
    '''
    The function takes input Excel file substractes relevant columns -'Structure',	'Name',	'Formula'. From the 'Structure'
    it create another  3 columns - inchikey, source_id , source_name. Then, take the JSON file which is
    the parsed data from the HMDB and merge the modified EXCEL with JSON, first by inchikey then by name and finely
    by Chemical Formula. This function takes the addinchikey and joindata functions  and merge them to one.
    :param excelpathin: The path to Excel file which is the output of the Compound Discoverer. in the format r'path' -
    r'D:/BCDD/Documents/TalCompounds_export_test.xlsx"
    :param jsonpathin: Path to JSON file - parsed XML file from HMDB
    :param excelpathout: Path to output Excel after the merge.
    :return: The columns of the Excel file with added columns  (disease name) from the JSON
    '''

    start_time = time.time()
#     CD = pd.read_excel(excelpathin)

    # data = pd.ExcelFile(r"C:\Users\USER\Downloads\MOD_REINJ_NEG_ChemSpider Results.xlsx")
    data = pd.ExcelFile(excelpathin)

    df = data.parse (sheet_name=0)
    inKey = list()
    for idx,sd in enumerate(df['Structure']):
        print(idx)
        F = open ("temp.sdf","w")
        F.writelines (sd)
        F.close()
        suppl = Chem.SDMolSupplier ('temp.sdf')
        mol = next (suppl)
        if mol==None:
            inKey.append (np.nan)
        else:
            inKey.append (Chem.MolToInchiKey (mol))

    inKey = pd.DataFrame(inKey)
    inKey.columns = ['InChIKey']
    CD = pd.concat([df, inKey], axis=1, sort=False)
    
    
    print("--- %s seconds --f-add 3 cols" % (time.time() - start_time))

    # From here is the joindata function with modification
    # Load the parse HMDB file
    with open(jsonpathin, 'r') as read_file:
        data = json.load(read_file)

    start_time = time.time()
    # Load the parse HMDB file
    # with open('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Output/serum_metabolites.json', 'r') as read_file:
    #     data = json.load(read_file)


    # Create a data frame from the list of dictionaries
    # df_hmdb = pd.DataFrame(data,  columns=['accession', 'name', 'chemical_formula', 'inchikey', 'disease_name' ])
    df_hmdb = pd.DataFrame(data)
    df_hmdb.drop(['description', 'synonyms', 'kegg_id', 'meta_cyc_id', 'pathway_name'], axis=1)

    df_excel = CD
    # Merge by inchikey
    joindata_by_inchikey = pd.merge(left=df_excel, right=df_hmdb, how='inner', left_on='InChIKey', right_on='inchikey')

    print("--- %s seconds --f-merge by inchikey " % (time.time() - start_time))

    start_time = time.time()
    # Reduce the rows to those we DID find a match by inchkey in bothe data sets
    df_hmdb_reduce_byinchik = df_hmdb.loc[~df_hmdb['inchikey'].isin(df_excel['InChIKey'])]
    df_excel_reduce_byinchik = df_excel.loc[~df_excel['InChIKey'].isin(joindata_by_inchikey['InChIKey'])]


    # joindata_by_name = fuzzymatcher.fuzzy_left_join(df_excel, df_hmdb, left_on="Name", right_on="name")
    joindata_by_name = fuzzymatcher.fuzzy_left_join(df_excel_reduce_byinchik, df_hmdb_reduce_byinchik, left_on="Name",
                                                    right_on="name")

    # Selecting threshold  best_match_score>0.25 maybe adjustments needed
    joindata_by_name = joindata_by_name[joindata_by_name['best_match_score'] > 0.55]
    # Drop columns the
    joindata_by_name.drop(['best_match_score', '__id_left', '__id_right'], axis=1, inplace=True)
    print("--- %s seconds --f-merge by name" % (time.time() - start_time))

    start_time = time.time()
    # Reduce the rows to those we DID find a match by inchkey in and by name both data sets
    df_hmdb_reduce_byname = df_hmdb_reduce_byinchik.loc[~df_hmdb_reduce_byinchik['name'].isin(joindata_by_name['name'])]
    df_excel_reduce_byname = df_excel_reduce_byinchik.loc[
        ~df_excel_reduce_byinchik['Name'].isin(joindata_by_name['Name'])]
    # Remove spaces between letters on  'Formula' ( there is  a warning)
    df_excel_reduce_byname.loc[:, 'Formula'] = df_excel_reduce_byname['Formula'].str.replace(' ', '')

    # Merge by chemical_formula
    joindata_by_CF = pd.merge(left=df_excel_reduce_byname, right=df_hmdb_reduce_byname, how='inner', left_on='Formula',
                              right_on='chemical_formula')

    # This data inculed rows from the original EXCEL file that we did NOT find and match ( by inchikey nor name nor CF)
    df_excel_reduce_byCF = df_excel_reduce_byname.loc[
        ~df_excel_reduce_byname['Formula'].isin(joindata_by_CF['chemical_formula'])]

    # Create a list of all columns of the HMDB JSON data
    colnames = joindata_by_inchikey.columns[6:]
    # Add those names as empty columns to the df_excel_reduce_byCF. reducedata in all the rows from the original Excel
    # that did NOT find a match and added the columns of the HMDB
    reducedata = df_excel_reduce_byCF.reindex(columns=[*df_excel_reduce_byCF.columns.tolist(), *colnames])

    # Append all the data sets
    # out = joindata_by_inchikey.append(joindata_by_name.append(joindata_by_CF))
    out = joindata_by_inchikey.append(joindata_by_name.append(joindata_by_CF.append(reducedata)))

    print("--- %s seconds --f-merge by CF" % (time.time() - start_time))
    # Export the merge data to an Excel file
    writer = pd.ExcelWriter(excelpathout, engine='xlsxwriter')
    # writer = pd.ExcelWriter('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/MOD_REINJ_NEG_ChemSpider ResultsW HMDB_0_1000.xlsx', engine='xlsxwriter')
    out.to_excel(writer, header=True)
    writer.save()
    writer.close()

    return (out)



if __name__ == "__main__":

    oupt= addcols_joindata(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/MOD_REINJ_NEG_ChemSpider Results.xlsx',
                     'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Output/serum_metabolites.json',
                     'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/MOD_REINJ_NEG_ChemSpider ResultsW HMDB_10001_2000.xlsx')
