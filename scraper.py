# import required modules
from bs4 import BeautifulSoup
import requests
import wikipedia
from chemicals import CAS_from_any, MW, Tb, Tm
import test_files.wikiChemObj as wikiChemObj
from dataMerger import dataMerger

# michiyo_wants_these_chemicals = input("What chemicals u want? Input separated by comma:\n")
# chemicals_list = michiyo_wants_these_chemicals.split(",")
# print(chemicals_list)

#################### CLASS WIKI SCRAPER ####################################


class wikiScraper:
    def __init__(self, query) -> None:
        self.query = query
        self.url = self.makeUrl()
        self.result_dict = {}
        self.content = ""
        
    @classmethod
    def wikiSearches(self, query):
        # returns a list of matching wikipedia articles from the input query
        try:
            results = wikipedia.search(query)
            return results
        except wikipedia.exceptions.DisambiguationError as e:
            return e.options

    @classmethod
    def wikiSummary(self, page_title):
        try:
            summary = wikipedia.summary(page_title)
            return summary
        except wikipedia.exceptions.DisambiguationError:
            return "You are as vague as a chameleon trying to hide in a room full of rainbows!"
        
    def getSoup(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def makeUrl(self):
        formatted_query = (self.query.strip()).capitalize().replace(' ','_')
        return ("https://en.wikipedia.org/wiki/" + formatted_query)

    def queryItem(self):
        myUrl = self.url
        myTable = self.getSoup(myUrl).find('table')
        data = self.scanTable(myTable)
        return data

    def scanTable(self, table):
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

    def extractValues(self, data, properties_list) -> dict:
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
    
    def dict_from_query(self, inquiry_list: list) -> dict:
        data = self.queryItem()
        prop_dict = self.extractValues(data=data, properties_list=inquiry_list)
        self.result_dict = prop_dict
        self.generateContentString()
        return prop_dict

    @classmethod
    def wikiSearchResults(self, query_list: list, interested_values: list) -> list:
        myList = []
        for inquiry in query_list:
            newScraper = wikiScraper(inquiry)
            newScraper.dict_from_query(interested_values)
            myList.append(newScraper)
        return myList
    
    def generateContentString(self):
        converted = ""
        for key, value in self.result_dict.items():
            converted += f"{key} | {value}\n"
        self.content = converted

##################### CHEMICAL - DATA ####################

    def chemicalsQuery(self):
        #CAS_chemical = search_chemical(chemical)
        try:
            CAS_chemical = CAS_from_any(self.query)
            
            molar_mass = MW(CAS_chemical)
            boiling_point = Tb(CAS_chemical)
            if(boiling_point is not None):
                boiling_point -= 273.15
            melting_point = Tm(CAS_chemical)
            if(melting_point is not None):
                melting_point -= 273.15
        except ValueError:
            print(f"Chemical name [{self.query}] not recognized")

        dictt = {
            "Molar mass":molar_mass,
            "Boiling point":boiling_point,
            "Melting point":melting_point,
        }
        self.result_dict = dictt
        self.generateContentString()
        return dictt

    @classmethod
    def chemicalsSearchResults(self, chemicals_list):
        myList = []
        for chemical_name in chemicals_list:
            newScraper = wikiScraper(chemical_name)
            newScraper.chemicalsQuery()
            myList.append(newScraper)
        return myList
    
################## MERGED DATA ###########################
    
    @classmethod
    def combinedSearchResults(self, chemicals_list, interested_list):
        myList = []
        for chemical_name in chemicals_list:
            newScraper = wikiScraper(chemical_name)
            dict1 = newScraper.dict_from_query(interested_list)
            dict2 = newScraper.chemicalsQuery()
            newScraper.result_dict = dataMerger.mergeDicts(dict1, dict2)
            newScraper.generateContentString()
            myList.append(newScraper)
        return myList

        

######################### END OF CLASS ####################################3

# def tryDict(dicto, stringer):
#     if dicto is not None:
#         try:
#             val = dicto[stringer]
#             print(f"Successful key: [{stringer}] - value: [{val}]")
#         except KeyError as err:
#             val = "😭"
#             print(f"Key [{stringer}] Does Not Exist in tryDict()")
#     else:
#         print("Dict is None!")
#         val = "😭"
#     return val    


# def populateClass(scraperClass: wikiScraper):
#     newObj = wikiChemObj.wikiChemObj(
#         name=scraperClass.query,
#         url=scraperClass.url,
#         dicto=prop_dict,
#         error="No Error",

#         molar_mass=tryDict(prop_dict, "Molar mass"),
#         density = tryDict(pr, "Density"),
#         colour = tryDict(pr, "Appearance"),
#         formula = tryDict(pr, "Chemical formula"),
#         solubility = tryDict(pr, "Solubility"),
#         sol_in_water = tryDict(pr, "Solubility in water"),
#         boiling_point = tryDict(pr, "Boiling point"),
#         melting_point = tryDict(pr, "Melting point")
#     )
#     return newObj

############# UNUSED CODE #################
#
# def dict_to_str(dict_to_print):
# # converts dict to a string which can be easily printed in discord
#     converted = str()
#     if dict_to_print is not None:
#         for key in dict_to_print:
#             converted += (key + ":   " + dict_to_print[key] + "\n")
#        
#     else:
#         converted = "No Data Found"
#     return converted
#
#
# def test_print_table(data):
# # for testing
#     df = pd.DataFrame(data, columns =['Property', 'Value']) 
#     print(df)
#
##########################################

