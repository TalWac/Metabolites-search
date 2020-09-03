from xml.dom import minidom
import xml.etree.ElementTree as et
import xmltodict

data = minidom.parse('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/saliva_metabolites/saliva_metabolites.xml')
data1 = et.parse('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/saliva_metabolites/saliva_metabolites.xml')
data3 = et.parse('D:/BCDD/Downloads/test.xml')
my_dict = xmltodict.parse('D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/saliva_metabolites/saliva_metabolites.xml')


ns = {
    "h": "http://www.hmdb.ca"
}
print(newlist)
dicts = {}
innerlist = []
newlist = []
for child in metabolites:
    innerlist = []
    dicts = {}
    for subchild in child:
        if subchild.tag=='{http://www.hmdb.ca}accession':
            dicts={"accession":  subchild.text}
            innerlist.append(subchild.text)
        elif  subchild.tag == '{http://www.hmdb.ca}name':
            dicts = {"name": subchild.text}
        # if subchild.tag == '{http://www.hmdb.ca}synonyms':
        #     for synonym in subchild:
        #         dicts = {"synonyms": synonym.text}
        #         print(synonym.text)
            innerlist.append(subchild.text)
            print(innerlist)

    newlist.append(dicts)

            innerlist.append(subchild.text)

        newlist.append(innerlist)

             print(subchild.text)



newlist = []
for x in range(10):
    innerlist = []
    for y in range(7):
        innerlist.append(y)
    newlist.append(innerlist)

print(newlist)

for child in metabolites:
    print(child.text)


for child in metabolites:
    if child.tag == "metabolite":
        print('oo')
        for step_child in child:
            print (step_child.tag)


for node in root:
    print(node.find('./h:metabolite', ns))

from lxml import etree
from pprint import pprint

news_sources = {
    source.attrib['source'] : [feed.text for feed in source.xpath('./f')]
    for source in etree.parse('D:/BCDD/Downloads/test.xml').xpath('/sources/sourceList')}

pprint(news_sources)

import xml.etree.ElementTree as ET
from pprint import pprint

news_sources = {
    source.attrib['source'] : [feed.text for feed in source]
    for source in ET.parse('D:/BCDD/Downloads/test.xml').getroot()}

pprint(news_sources)




root = data1.getroot()
# extract the value
root[0][3].text


for node in root:
    print(node.find('accession').text)

print(root[0][1].attrib)

for child in root[0:2][1]:
    print (child.tag, child.attrib)

for elem in root:
    for subelem in elem:
        print(subelem.attrib)

for elem in root:
    print(elem.find('metabolite'))

for elem in root:
    for subelem in elem.findall('metabolite'):

for child in root:
        print(child.find('metabolite').text)

root.findall('./metabolite/accession')
for elem in root[0].iter('synonyms'):
            value = elem.text


for elem in root[0].iter('synonyms'):
    for subelem in elem.root[0].iter('*'):

            print(subelem.text)

 for metabolite in root.findall('metabolite'):

     accession = metabolite.find('accession').text

     print (accession)
for elem in root[0].iter('*'):
    for subelem in elem:
        print(subelem.text)
root.child()
# dataroot = data.getroot()
# xtree = et.parse("D:/BCDD/Documents/Tal/Projects/HMDB/DataSets/saliva_metabolites/saliva_metabolites.xml")
#
# root = tree.getroot()
# metabolites = data.getElementsByTagName('metabolite')
#print(metabolites[1])
# print(1+1)
for child in root:
    print (child.tag, child.attrib)


def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    # create empty list for news items
    newsitems = []

    # iterate news items
    for item in root.findall('./channel/item'):

        # empty news dictionary
        news = {}

        # iterate child elements of item
        for child in item:

            # special checking for namespace object content:media
            if child.tag == '{http://search.yahoo.com/mrss/}content':
                news['media'] = child.attrib['url']
            else:
                news[child.tag] = child.text.encode('utf8')

                # append news dictionary to news items list
        newsitems.append(news)

        # return news items list
    return newsitems
