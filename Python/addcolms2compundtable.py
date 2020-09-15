import pandas as pd
import pubchempy as pcp
import time
r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Compounds_export_test.xlsx'
# CD = pd.read_excel(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Compounds_export_test.xlsx')

def addinchikey(excelpathin, excelpathout):
    '''
    The function takes input Excel file substractes relevant columns -'Structure',	'Name',	'Formula'. From the 'Structure'
    it create another  3 columns - inchikey, source_id , source_name
    :param excelpathin: The path to Excel file which is the output of the Compound Discoverer. in the format r'path' -
    r'D:/BCDD/Documents/TalCompounds_export_test.xlsx"
    :param excelpathout: path to output Excel after the merge.
    :return: Excel file with inchikey
    '''

    CD = pd.read_excel(excelpathin)
    CD = pd.DataFrame(CD, columns=['Structure', 'Name', 'Formula'])
    sdflist = CD.Structure

    # loop over all cells in Structure is Nan value enter the string 'Nan'
    # adding delay time so we want be blocked
    newlistinchikey = []
    newlistsource_id = []
    newlistsource_name = []
    for idx, sdf in enumerate(sdflist):

        if idx % 50 == 0:
            time.sleep(3.25)

        if pd.isnull(sdf):
            # print(idx)
            newlistinchikey.append('Nan')
            newlistsource_id.append('Nan')
            newlistsource_name.append('Nan')
        else:
            comp = pcp.get_compounds(sdf, 'sdf')
            substance = pcp.get_substances(comp[0].cid, 'sid')
            # print(comp)
            # print(substance)
            # comp[0].inchikey
            newlistinchikey.append(comp[0].inchikey)
            newlistsource_name.append(substance[0].source_name)
            newlistsource_id.append(substance[0].source_id)

    # Change list to Dataframe and concatenate with the original data and name them
    newlistinchikey = pd.DataFrame(newlistinchikey)
    newlistinchikey.columns = ['inchikey']
    newlistsource_name = pd.DataFrame(newlistsource_name)
    newlistsource_name.columns = ['source_name']
    newlistsource_id = pd.DataFrame(newlistsource_id)
    newlistsource_id.columns = ['source_id']

    CD = pd.concat([CD, newlistinchikey, newlistsource_name, newlistsource_id],   axis=1, sort=False)

    # Export the merge data to an Excel file
    writer = pd.ExcelWriter(excelpathout, engine='xlsxwriter')

    CD.to_excel(writer,  header=True)
    writer.save()
    writer.close()

if __name__ == "__main__":

    addinchikey(r'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Compounds_export_test.xlsx',
                'D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/Compounds_export_testW 3cols.xlsx')