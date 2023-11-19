class wikiChemObj:
    def __init__(self, name=None, molar_mass=None, boiling_point=None,
                  melting_point=None, density=None, colour=None, formula=None,
                    solubility=None, sol_in_water=None, error=None, url=None) -> None:
        
        self.name = name
        self.molar_mass = molar_mass
        self.boiling_point = boiling_point
        self.melting_point = melting_point
        self.density = density
        self.colour = colour
        self.formula = formula
        self.solubility = solubility
        self.sol_in_water = sol_in_water
        self.error = error
        self.url = url
        self.content = self.ObjToString()

        self.dicto


    ############## UNUSED CODE ##############
    #
    # def ObjToDict(self):
    #     newDict = {
    #         "Formula":self.formula,
    #         "Density":self.density,
    #         "Molar Mass":self.molar_mass,
    #         "Colour":self.colour,
    #         "Boiling Point":self.boiling_point,
    #         "Melting Point":self.melting_point,
    #         "Solubility":self.solubility,
    #         "Sol. in water":self.sol_in_water
    #     }
    #     return newDict
    #
    ##########################################

    @classmethod
    def ObjToString(self):
        converted = f"""
```\n
Formula       | {self.formula}
Density       | {self.density}
Molar Mass    | {self.molar_mass}
Colour        | {self.colour}
Boiling Point | {self.boiling_point}
Melting Point | {self.melting_point}
Solubility    | {self.solubility}
Sol. in water | {self.sol_in_water} \n
```
        """
        return converted