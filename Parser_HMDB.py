import xml.etree.ElementTree as et

data1 = et.parse('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/saliva_metabolites/saliva_metabolites.xml')
root = data1.getroot()

xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

with open('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/saliva_metabolites/saliva_metabolites.xml') as fd:
    doc = xmltodict.parse(fd.read())


ns = {"h": "http://www.hmdb.ca"}

# extract the first 3 metabolites
metabolites = root.findall('./h:metabolite', ns)    # [0:3]


for accession in root.findall('./h:metabolite/h:accession', ns):
    print(accession.text)

outp=[]
for child in metabolites:
    for subchild in child:
        print   (subchild.tag)

for elem in metabolites[0]:
    print(elem.text)


 for elem in metabolites[0]:
    for subelem in elem:
        print(elem.text)

news_sources = {}

for elem in root:
    elem = elem.attrib['source']
    news_sources[sourceListName] = []

    for synonym in metabolites[0][9]:
       synonymName = synonym.text

    prices_look = [{'apple': 2.99, 'orange': [1, 2, 3], 'milk': 'tal'},
                   {'apple': 2.99, 'orange': [1, 2, 3], 'milk': 'tal'}]     news_sources[sourceListName].append(synonymName)