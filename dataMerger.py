# Merges data from two different sources.
# data1 and data2 are both list of objects DataObj
# the result will also be a list of DataObj objects, but with combined data of the two sources
# Final DataObj data is selected based on "if not None" conditions
# the argument dataVariables is a list of names of DataObj variables which should be merged
# Choose a default value if no Data is found with parameter default_ND

class dataMerger:

    mergedData = []

    def __init__(self) -> None:
        self.default_ND = "N/D"

    @classmethod
    def mergeClasses(self, dataObj, data1: list, data2: list, dataVariables: list) -> list:

        # Initialize a list to store merged DataObj instances
        merged_data = []

        # Iterate through the data from both sources simultaneously
        for obj1, obj2 in zip(data1, data2):
            if obj1 and obj2:
                # Create a new DataObj instance for merging
                merged_obj = dataObj()

                # Merge data variables based on the dataVariables list
                for variable in dataVariables:
                    value1 = getattr(obj1, variable, self.default_ND)
                    value2 = getattr(obj2, variable, self.default_ND)

                    # Select data based on "if not None" conditions
                    if value1 is not None:
                        setattr(merged_obj, variable, value1)
                    else:
                        setattr(merged_obj, variable, value2)

                # Add the merged DataObj to the result
                merged_data.append(merged_obj)
            elif obj1:
                    merged_data.append(obj1)
            elif obj2:
                merged_data.append(obj2)            

        return merged_data
    
    @classmethod
    def mergeDicts(self, dict1: dict, dict2: dict) -> dict:
        # Initialize the merged dictionary
        merged_dict = {}

        # Merge data from dict1
        for key, value in dict1.items():
            if value is not None:
                merged_dict[key] = value

        # Merge data from dict2, taking value if not None
        for key, value in dict2.items():
            if value is not None:
                merged_dict[key] = value

        return merged_dict





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
