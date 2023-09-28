class wikiChemObj:
    def __init__(self, content, name, molar_mass, boiling_point, melting_point, density, colour, formula, solubility, sol_in_water, error, url) -> None:
        self.content = content
        self.error = error
        self.name = name
        self.density = density
        self.colour = colour
        self.formula = formula
        self.solubility = solubility
        self.sol_in_water = sol_in_water
        self.molar_mass = molar_mass
        self.boiling_point = boiling_point
        self.melting_point = melting_point
        self.url = url

    def ObjToDict(self):
        newDict = {
            "Formula":self.formula,
            "Density":self.density,
            "Molar Mass":self.molar_mass,
            "Colour":self.colour,
            "Boiling Point":self.boiling_point,
            "Melting Point":self.melting_point,
            "Solubility":self.solubility,
            "Sol. in water":self.sol_in_water
        }
        return newDict

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