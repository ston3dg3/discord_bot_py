
###################################################################################
###################################################################################

# def mergeData(myList):
#     newList=[]
#     print("mergeData initiated!!!")
#     wikiList = wikiScrapeChem(myList)
#     chemList = query_chemicals(myList)
#     print("=============== WIKI LIST ===================")
#     for x in wikiList:
#         print(x.content)
#         print(x.error)
#         print(x.molar_mass)
#     print("=============  CHEM LIST  ======================")
#     for x in chemList:
#         print(x.content)
#         print(x.error)
#         print(x.molar_mass)
#     print("=======================================")

#     for idx, chemical in enumerate(wikiList):

#         melt = None
#         boil = None
#         boil = wikiList[idx].boiling_point if (wikiList[idx].boiling_point is not None) else chemList[idx].boiling_point
#         melt = wikiList[idx].melting_point if (wikiList[idx].melting_point is not None) else chemList[idx].melting_point
#         MolMass = chemList[idx].molar_mass if (chemList[idx].error != "Error") else chemical.molar_mass
            

#         newObj = wikiChemObj.wikiChemObj(
#             name=wikiList[idx].name,
#             content=None,
#             error=chemList[idx].error,
#             url=wikiList[idx].url,

#             molar_mass = str(MolMass),
#             melting_point=melt,
#             boiling_point=boil,
#             density=wikiList[idx].density,
#             colour=wikiList[idx].colour,
#             formula=wikiList[idx].formula,
#             solubility=wikiList[idx].solubility,
#             sol_in_water=wikiList[idx].sol_in_water
#         )

#         newList.append(newObj)
#     return newList

##################################################################################


# class bot_parameters:

#     @classmethod
#     def getIntents(self):
#         bot_intents = Intents.default()
#         bot_intents.members = True
#         bot_intents.message_content = True
#         return bot_intents
    
    

#     messageCountChannelID = 1152392328699461682
    
#     savedMessageChannelID = 1152273521028898856

#     bot_prefix = "$"

#     bot_description = "Michiyo is a pufferfish"

#     swear_words = [
#         "asian", "white", "black", "nigger", "nigga", "racist"
#     ]

#     count_list = [
#         "bb", "cow", "asian", "white", "tortle", "neko", "racist",
#         "tummy", "pee"
#     ]
    
#     swear_notice1 = "Hi Franek dont be racist bc michiyo will get mad at u"

#     swear_notice2 = """
#         Dear Discord User,
#         I hope this message finds you well. We appreciate your presence on our Discord server and value your contributions to our community. However, we've noticed that there have been instances of swearing in your recent messages.
#         Our server is committed to providing a welcoming and respectful environment for all members, and as such, we have a policy against the use of explicit language. We kindly request that you refrain from swearing in the future to maintain the positive atmosphere we strive to create.
#         We understand that slips can happen, but repeated violations may lead to more serious actions, such as a temporary mute or, in extreme cases, removal from the server. We sincerely hope it doesn't come to that and would prefer to continue enjoying your presence here.
#         If you have any questions or concerns regarding our server rules or any other matter, please feel free to reach out to one of our moderators or administrators. They are always ready to assist you.
#         Thank you for your understanding and cooperation in this matter. Let's work together to keep our server a pleasant place for everyone.
#         Best regards,
#         Server Administration (and Tortle)
#                     """
    
#     chem_attributes_list = [
#         'Chemical formula', 'Molar mass', 'Appearance', 'Density', 
#         'Melting point', 'Boiling point', 'Solubility', 'Solubility in water'
#     ]


###############################################


################ TESTING ZONE ##########################################

# class testObject():
#     def __init__(self, name=None, age=None, colour=None, error=None, test=None) -> None:
#         self.name = name
#         self.age = age
#         self.colour = colour
#         self.error = error
#         self.test = test
    
#     def __str__(self) -> str:
#         return f"""testObject:
#             name: {self.name}
#             age: {self.age}
#             colour: {self.colour}
#             error: {self.error}
#             test: {self.test}
# """

# data1 = [testObject(age=22, colour=0xadf542, error="No Error", test="test"), 
#          testObject(name="Tom", error="No Error")]

# data2 = [testObject(name="Sarah", age=22, error="Error"),
#          testObject(test="YAYY") ]


# merged = mergeData(testObject, data1=data1, data2=data2, dataVariables=["name", "age", "colour"], default_ND="N/D")
# [print(x) for x in merged]

########################################################################

