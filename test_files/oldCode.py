











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