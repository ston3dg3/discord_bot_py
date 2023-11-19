# File containing utility functions for manipulating strings etc...
import json
import re
import time
from datetime import datetime
import exceptions

# TODO: turn utilities into global functions SMH

def add_word_to_count( new_word):
    count_word = {
        "word": new_word,
        "count": 0
    }
    json_obj = json.dump(count_word, indent=4)
    file = open("word_count.txt", "a")
    file.write(json_obj)
    file.close()


def swear_word( message):
    from bot_setup import swear_words
    msg = message.content
    return any(ele in msg for ele in swear_words)


def count_word( message, mess_list):
    # upper matching also indcludes elements within other strings.
    # matching_element = next((element for element in mess_list if element in message.content), None)
    matching_element = next((element for element in mess_list if re.search(rf'\b{element}\b', message.content)), None)
    if matching_element:
        return matching_element


def add_to_txt( message):
    msg = message.content
    f = open('fav_list.txt', 'a')
    f.write(msg)
    f.write('\n')
    f.close()


def clamp( n, minn, maxn):
    return max(min(maxn, n), minn)


def tryDict( dict, stringer):
    try:
        val = dict[stringer]
    except KeyError:
        val = "N/D"
    return val


def cast(value, data_type: str):
    # Define a list of allowed data types for casting
    allowed_types = ['int', 'float', 'str', 'list', 'dict', 'bool']

    # Check if the specified data type is in the allowed types
    if data_type in allowed_types:
        try:
            # Use eval() to perform the type casting
            return eval(f'{data_type}({value})')
        except (ValueError, SyntaxError):
            return None  # Handle invalid conversions
    else:
        return None  # Data type not allowed
    

# Takes required argument and user argument
# Converts user argument to the required argument type (if specified)
# Check if user argument has required length (if specified) 
# SCHEMA for sepcifying required arguemnts: name:type:length
# name can be anything, it does not play a role unless there is a star (*) in front
# star in front of name means all arguments after this one will be interpreted as one variable
# def parseArg(arg, user_arg: str):
#     if user_arg is None or not isinstance(user_arg, str):
#         return
#     length = arg.count(":")

#     if length == 0:
#         # No checks
#         if [0] == "*":
#             return "*"+user_arg
#         return user_arg
#     elif length == 1:
#         # only type cast
#         params = arg.split(":")
#         name = params[0]
#         type = params[1]
#         # cast user argument to type
#         user_arg = cast(user_arg, type)
#         return user_arg
#     elif length == 2:
#         # type cast user argument and length check
#         params = arg.split(":")
#         name = params[0]
#         type = params[1]
#         len = params[2]
#         # type cast user argument to type
#         user_arg = cast(user_arg, type)
#         # check length of name
#         if (len(user_arg) == len):
#             # all good - length matching
#             return user_arg
#         else:
#             # the length does not match the required argument length
#             raise exceptions.ParsingLenghtInvalid
#     else:
#         raise exceptions.ParsingTooManyDelimeters
    

class ParsingError(Exception):
    pass

def parse(commands, user_arguments):
    parsed_arguments = []

    try:
        # Iterate through the command definitions
        for command in commands:
            required_options, required_arguments = command

            # Check if the user's input matches any of the required options
            if user_arguments and user_arguments[0] not in required_options:
                continue  # No matching command found

            # Extract user arguments (excluding the command)
            user_args = user_arguments[1:]

            # Check if the number of user arguments matches the number of required arguments
            if len(user_args) < len([arg for arg in required_arguments if not arg.startswith("*")]):
                raise ParsingError("Not enough arguments provided")

            parsed_command = []
            long_string = None

            for i in range(len(required_arguments)):
                arg_definition = required_arguments[i].split(":")
                arg_name = arg_definition[0]
                arg_type = arg_definition[1] if len(arg_definition) > 1 else None
                arg_length = arg_definition[2] if len(arg_definition) > 2 else None

                if arg_name.startswith("*"):
                    # Treat all subsequent arguments as one long string
                    long_string = " ".join(user_args[i:])
                    break  # Exit the loop as all subsequent arguments are part of the long string

                user_arg = user_args[i]

                if arg_type:
                    try:
                        if arg_type == "str":
                            if arg_length and len(user_arg) != int(arg_length):
                                raise ParsingError(f"Invalid length of argument {arg_name}")
                            user_arg = str(user_arg)
                        elif arg_type == "int":
                            user_arg = int(user_arg)
                        elif arg_type == "float":
                            user_arg = float(user_arg)
                        elif arg_type == "bool":
                            if user_arg.lower() in ("true", "false"):
                                user_arg = user_arg.lower() == "true"
                            else:
                                raise ParsingError("Invalid boolean value")
                        else:
                            raise ParsingError("Invalid argument type")

                        parsed_command.append(user_arg)
                    except (ValueError, TypeError):
                        raise ParsingError(f"Invalid argument {arg_name}")
                else:
                    parsed_command.append(user_arg)

            if long_string:
                parsed_command.append(long_string)

            # If the loop completes, all arguments are valid
            parsed_arguments.extend(parsed_command)
    except ParsingError as e:
        print(e)
        # Exit the program or take any necessary actions here

    if parsed_arguments is not None:
        return parsed_arguments
    else:
        raise ParsingError("Parsing Error Occured")


# EXAMPLE COMMANDS DEFINITION
# commands = [
#     [["list"], []],
#     [["help"], []],
#     [["add"], ["name:str", "alphabet:str:26"]],
#     [["style"], ["name", "*message"]]
# ]



    

    
###### WRAPPERS ############# DECORATORS ##########################
    
def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        func(*args, **kwargs)
        print(f"Function {func.__name__} took {(time.time()-before)} seconds")
    return wrapper

def log(func):
    def wrapper(*args, **kwargs):
        with open('logs.txt', 'a') as f:
            f.write("Called function \"" + func.__name__ + "\" with [ " + " ".join([str(arg) for arg in args]) + " ] at "+str(datetime.datetime.now()) + "\n")
        val = func(*args, **kwargs)
        return val    
    return wrapper
    
#####################################################################