import json
import csv
import os
import sys
from rdkit import Chem
# import rdkit.Chem
# import rdkit
import numpy as np
import pandas as pd
import pickle
import time
import fuzzymatcher
from CdScriptingNodeHelper import ScriptingResponse


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


#
# Scripting Node for Compound Discoverer that calculates difference in Features Molecolar Weigth against m/z
#

def main():
    print('CD Scripting Node')

    # start in development mode where nodeargs are given explicitely rather than reading it as command line argument
    if sys.argv[1] == '-devel':
        print(f'Development mode: Current Dir is {os.getcwd()}')
        nodeargs_path = 'node_args.json'
    else:
        nodeargs_path = sys.argv[1]

    # parse node args from Compound Discoverer and extract location of ChemSpider Results table
    try:
        with open(nodeargs_path, 'r') as rf:
            nodeargs = json.load(rf)
            features_path = ''
            response_path = nodeargs['ExpectedResponsePath']
            tables = nodeargs['Tables']
            for table in tables:
                if table['TableName'] == 'ChemSpider Results':
                    features_path = table['DataFile']
                    if table['DataFormat'] != 'CSV':
                        print_error(f"Unknown Data Format {table['DataFormat']}")
                        exit(1)
    except Exception as e:
        print_error('Could not read Compound Discoverer node args')
        print_error(str(e))
        exit(1)

    if not features_path:
        print_error('ChemSpider Results file not defined in node args.')
        exit(1)

    try:
    # if 1 > 0:
        with open(features_path, mode='r') as protFile:
            reader = csv.DictReader(protFile, delimiter='\t')
            df = pd.DataFrame(reader)

            inKey = list()
            for idx, sd in enumerate(df['Structure']):
                # print(idx)
                F = open("temp.sdf", "w")
                F.writelines(sd)
                F.close()
                suppl = Chem.SDMolSupplier('temp.sdf')
                mol = next(suppl)
                if mol == None:
                    inKey.append(np.nan)
                else:
                    inKey.append(Chem.MolToInchiKey(mol))

            inKey = pd.DataFrame(inKey)
            inKey.columns = ['InChIKey']
            CD = pd.concat([df, inKey], axis=1, sort=False)

    # Load the parse HMDB file
        with open('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Parser_HMDB.py Output/hmdb_metabolites.json', 'r') as read_file:
            data = json.load(read_file)

        df_hmdb = pd.DataFrame(data)
        df_hmdb.drop(['description', 'synonyms', 'kegg_id', 'meta_cyc_id', 'pathway_name'], axis=1)

        df_excel = CD

        # Remove spaces between letters on  'Formula' ( there is  a warning)
        CD = CD.copy()
        CD.loc[:, ('Formula')] = CD['Formula'].str.replace(" ", "")

        joindata_by_inchikey = pd.merge(left=df_excel, right=df_hmdb, how='inner', left_on='InChIKey', right_on='inchikey')
        # Reduce the rows to those we DID find a match by inchkey in bothe data sets
        df_hmdb_reduce_byinchik = df_hmdb.loc[~df_hmdb['inchikey'].isin(df_excel['InChIKey'])]
        df_excel_reduce_byinchik = df_excel.loc[~df_excel['InChIKey'].isin(joindata_by_inchikey['InChIKey'])]

        # joindata_by_name = fuzzymatcher.fuzzy_left_join(df_excel, df_hmdb, left_on="Name", right_on="name")
        joindata_by_name = fuzzymatcher.fuzzy_left_join(df_excel_reduce_byinchik, df_hmdb_reduce_byinchik, left_on="Name",
                                                        right_on="name")
        # Selecting threshold  best_match_score>0.25 maybe adjustments needed
        joindata_by_name = joindata_by_name[joindata_by_name['best_match_score'] > 0.85]

        # Drop columns the
        joindata_by_name.drop(['best_match_score', '__id_left', '__id_right'], axis=1, inplace=True)

        # Reduce the rows to those we DID find a match by inchkey in and by name both data sets
        df_hmdb_reduce_byname = df_hmdb_reduce_byinchik.loc[
            ~df_hmdb_reduce_byinchik['name'].isin(joindata_by_name['name'])]
        df_excel_reduce_byname = df_excel_reduce_byinchik.loc[
            ~df_excel_reduce_byinchik['Name'].isin(joindata_by_name['Name'])]

        # Merge by chemical_formula
        joindata_by_CF = pd.merge(left=df_excel_reduce_byname, right=df_hmdb_reduce_byname, how='inner', left_on='Formula',
                                  right_on='chemical_formula')
        # This data inculed rows from the original EXCEL file that we did NOT find and match ( by inchikey nor name nor CF)
        df_excel_reduce_byCF = df_excel_reduce_byname.loc[
            ~df_excel_reduce_byname['Formula'].isin(joindata_by_CF['chemical_formula'])]

        # Create a list of all columns of the HMDB JSON data
        colnames = joindata_by_inchikey.columns[13:]

        # Add those names as empty columns to the df_excel_reduce_byCF. reducedata in all the rows from the original Excel
        # that did NOT find a match and added the columns of the HMDB
        reducedata = df_excel_reduce_byCF.reindex(columns=[*df_excel_reduce_byCF.columns.tolist(), *colnames])

        out = joindata_by_inchikey.append(joindata_by_name.append(joindata_by_CF.append(reducedata)))

        # remove duplicates columns names
        out = out.drop(columns=['name', 'smiles', 'inchikey'])

        # out = out.drop(out.iloc[:,30: ])
        out.columns = [x.strip() for x in out.columns]
        # out =out.loc[: ,"ChemSpider Results CSID":"Thyroid cancer"]
    except Exception as e:
        print_error('Could not process data')
        print_error(e)
        exit(1)

    # write data file
    outfilename = "ChemSpiderResultsWithInChIKey.txt"
    (workdir, _) = os.path.split(response_path)
    outfile_path = os.path.join(workdir, outfilename)
    out.to_csv(outfile_path, sep='\t', index=False)

    # entries for new column in Features table
    response = ScriptingResponse()
    response.add_table('ChemSpider Results', outfile_path)

    # select only the columns we want to add
    for indx, colname in enumerate(out.columns[12:]):
        response.add_column('ChemSpider Results', colname, 'String')
        # print(indx, colname)

    # save to disk
    response.save(response_path)


if __name__ == "__main__":
    main()