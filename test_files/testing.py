import time
import datetime
import wikipedia

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

def tryDict(func):
    def wrapper(dicto, stringer):
        try:
            val = dicto[stringer]
        except KeyError as err:
            val = "😭"
        return val    
    return wrapper



# @timer
# @log
# def run(a, b, c=4):
#     time.sleep(2)

# run(2, 3)


def parse(commands, user_arguments):
    parsed_arguments = []
    
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
            print("Not enough arguments provided")
            continue  # Argument count doesn't match

        parsed_command = []
        long_string = None
        
        for i in range(len(required_arguments)):
            arg_name, arg_type, arg_length = required_arguments[i].split(":")
            
            if arg_name.startswith("*"):
                # Treat all subsequent arguments as one long string
                long_string = " ".join(user_args[i:])
                break  # Exit the loop as all subsequent arguments are part of the long string
            
            user_arg = user_args[i]
            
            try:
                if arg_type == "str":
                    if arg_length and len(user_arg) != int(arg_length):
                        print(f"Invalid length of argument {arg_name}")
                        raise ValueError("Invalid argument length")
                elif arg_type == "int":
                    user_arg = int(user_arg)
                elif arg_type == "float":
                    user_arg = float(user_arg)
                elif arg_type == "bool":
                    if user_arg.lower() in ("true", "false"):
                        user_arg = user_arg.lower() == "true"
                    else:
                        raise ValueError("Invalid boolean value")
                else:
                    raise ValueError("Invalid argument type")

                parsed_command.append(user_arg)
            except (ValueError, TypeError):
                continue  # Invalid argument, continue with the next command
        
        if long_string:
            parsed_command.append(long_string)

        # If the loop completes, all arguments are valid
        parsed_arguments.extend(parsed_command)
    
    return parsed_arguments

# Example usage:
commands = [
    [["list"], []],
    [["help"], []],
    [["add"], ["name:str:3", "alphabet:str:24"]],
    [["style"], ["name:str:5", "*message"]],
    [[], ["name:str", "*message"]]
]

user_arguments = ["style", "green", "this", "is", "a", "longer", "message"]
parsed_arguments = parse(commands, user_arguments)
print(parsed_arguments)


    

