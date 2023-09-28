from chemicals import CAS_from_any, MW, Tb, Tm
import wikiChemObj

# michiyo_wants_these_chemicals = input("What chemicals u want? Input separated by comma:\n")
# chemicals_list = michiyo_wants_these_chemicals.split(",")
# print(chemicals_list)

def query_chemicals(chemicals_list):
    print("query chemicals initiated!")

    chem_list = []
    for chemical in chemicals_list:

        #CAS_chemical = search_chemical(chemical)
        try:
            CAS_chemical = CAS_from_any(chemical)
            
            molar_mass = MW(CAS_chemical)
            boiling_point = Tb(CAS_chemical)
            if(boiling_point is not None):
                boiling_point -= 273.15
            melting_point = Tm(CAS_chemical)
            if(melting_point is not None):
                melting_point -= 273.15
            newObj = populateClass(name=chemical, melt=melting_point, boil=boiling_point, mass_molar=molar_mass)

        except ValueError:
            newObj = populateClass(name=chemical, content=f"Chemical name [{chemical}] not recognized", error="Error")
        
        chem_list.append(newObj)

    return chem_list

def populateClass(name, content=None, error="No Error", melt=None, boil=None, mass_molar=None):
    newObj = wikiChemObj.wikiChemObj(
        name=name,
        content=content, 
        url=None, 
        error=error,

        molar_mass=mass_molar,
        density=None,
        colour=None,
        formula=None,
        solubility=None,
        sol_in_water=None,
        melting_point=melt,
        boiling_point=boil
    )
    return newObj
