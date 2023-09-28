# import required modules
from bs4 import BeautifulSoup
import requests
import pandas as pd
import wikiChemObj
        
def getSoup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def makeUrl(query):
    formatted_query = (query.strip()).capitalize().replace(' ','_')
    return ("https://en.wikipedia.org/wiki/" + formatted_query)

def queryItem(query):
    myUrl = makeUrl(query)
    myTable = getSoup(myUrl).find('table')
    data = scanTable(myTable)
    return data

def scanTable(table):
# converts html table to 2D array
    data = []
    for row in table.find_all('tr'):

        cols = row.find_all('td')
        # Extracting the table headers
        if len(cols) == 0:
            cols = row.find_all('th')

        cols = [ele.text.strip() for ele in cols]
        if(len(cols) <= 2):
            data.append([ele for ele in cols if ele])  # Get rid of empty values

    return data

def extractValues(data, properties_list):
# extract wanted properties from scanned Table data
    properties_dict = {}
    if data is not None:
        print("============ wiki scraper table ==========")
        print(data)
        print("===========================================")
        try:
            for row in data:
                if(len(row) == 2 and row[0] in properties_list):
                    print(row[0]+"\n")
                    keyy = row[0] if (row[0]!=None) else "unknown"
                    valuee = row[1] if (row[1]!=None) else "😭"
                    properties_dict.update({keyy:valuee})
        except IndexError:
            properties_dict = None
            print("!!! Index Error !!!")
    else:
        properties_dict = None

    print("============ wiki scraper DICT ==========")
    print(properties_dict)
    print("===========================================")
    return properties_dict

def tryDict(dicto, stringer):
    if dicto is not None:
        try:
            val = dicto[stringer]
            print(f"Successful key: [{stringer}] - value: [{val}]")
        except KeyError as err:
            val = "😭"
            print(f"Key [{stringer}] Does Not Exist in tryDict()")
    else:
        print("Dict is None!")
        val = "😭"
    return val    


def populateClass(pr, name, content, url):
    newObj = wikiChemObj.wikiChemObj(
        name=name,
        content=content, 
        url=url,
        error="No Error",

        molar_mass=tryDict(pr, "Molar mass"),
        density = tryDict(pr, "Density"),
        colour = tryDict(pr, "Appearance"),
        formula = tryDict(pr, "Chemical formula"),
        solubility = tryDict(pr, "Solubility"),
        sol_in_water = tryDict(pr, "Solubility in water"),
        boiling_point = tryDict(pr, "Boiling point"),
        melting_point = tryDict(pr, "Melting point")
    )
    return newObj

def dict_to_str(dict_to_print):
# converts dict to a string which can be easily printed in discord
    converted = str()
    if dict_to_print is not None:
        for key in dict_to_print:
            converted += (key + ":   " + dict_to_print[key] + "\n")
        
    else:
        converted = "No Data Found"
    return converted


def test_print_table(data):
# for testing
    df = pd.DataFrame(data, columns =['Property', 'Value']) 
    print(df)



######################## MAIN PROGRAM #####################################

# add items for more search results :P
moja_lista = [
    'Chemical formula', 'Molar mass', 'Appearance', 'Density', 
    'Melting point', 'Boiling point', 'Solubility', 'Solubility in water'
    ]

def wikiScrapeChem(inquiry_list):
    print("wikiScrapeChem initiated")
    myList = []
    for inquiry in inquiry_list:
        data = queryItem(inquiry)
        dictt = extractValues(data=data, properties_list=moja_lista)
        strr = dict_to_str(dictt)
        obj = populateClass(pr = dictt, name=inquiry, content=strr, url=makeUrl(inquiry))
        myList.append(obj)
    return myList
        
#print(wikiScrapeChem("Hydrogen Chloride"))

