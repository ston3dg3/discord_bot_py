import bot_setup
import exceptions
import utilities


class cmd_parser():
    def __init__(self, cmd_name: str, cmds: list) -> None:

        self.cmd_name = cmd_name
        self.cmds = cmds
        if(not self.is_3d_list_of_str() or (not isinstance(cmd_name, str))):
            raise exceptions.CommandArgsWrongType
        
        
    def printPossibleCMDs(self):
        pass


    # FIND MATCHING SUBCOMMAND by searching first option
    # 


    # returns "SUCCESS" if successful, othwerwise a string error message
    def parse(self, args):
        args = args[1:]
        parsed_args = []
        subcommand_found = False

        for subcommand in self.cmds:
            if subcommand_found:
                break
            # from this point we are inspecting a single subcommand
            options = subcommand[0]
            
            if options is not None:
                for i in range(len(options)):
                    opts_fail = []
                    if args[i] == options[i]:
                        # The chosen option exists at the right position :)
                        # From now on only work with found command
                        self.cmds = subcommand

                        opts_fail.append(args[i])
                        subcommand_found = True
                    else:
                        break
                print(opts_fail)

        if subcommand_found == False and options is not None:
            strr = " ".join(opts_fail)
            return f"The option [{bot_setup.bot_prefix}{cmd_name} {strr}] is invalid. Please see [{bot_setup.bot_prefix}{cmd_name} help] for help"

        args = args[len(options):] 
        for arrr in args: print(arrr)

        for subcommand in self.cmds:
            options = subcommand[0]
            arguments = subcommand[1]    
            for arrr in arguments: print(arrr)
            for i in range(len(arguments)):
                if args[i]:
                    # The given argument is valid :)
                    for arrr in arguments: print(arrr)
                    for arrr in args: print(arrr)
                    parsed_arg = utilities.parseArg(arguments[i-len(options)], args[i])
                    # if the last argument starts with a star, treat all next arguments as one long string
                    # No need to parse them because they cant be anything...
                    if parsed_arg[0] == "*":
                        parsed_args.append(" ".join(args[i-len(options)-1:]))
                        return parsed_args
                    parsed_args.append(parsed_arg)
                else:
                    return f"Too few arguments specified. Please see [{bot_setup.bot_prefix}{cmd_name} help] for help"
            return parsed_args
                    

    def is_3d_list_of_str(self):
        if isinstance(self.cmds, list):
            # Check if it's a 3D list
            for i in self.cmds:
                if isinstance(i, list):
                    for j in i:
                        if isinstance(j, list):
                            for k in j:
                                if isinstance(k, str):
                                    return True
                                

                             
cmd_name = "font"



cmds = [
    [["list"],[]],
    [["help"],[]],
    [["add"], ["name:str", "alphabet:str:24"]],
    [["style"], ["name:str", "*message"]],
    [[],["name", "*message"]]
]
# each line is one possible command
# first inner list specifies the required options for the command
# second inner list specifies the required arguments for the command
# if one of the inner lists is empty, the options/arguemnts are not required.
# SCHEMA for sepcifying required arguemnts: name:type:length
# name can be anything, it does not play a role unless there is a star (*) in front
# star in front of name means all arguments after this one will be interpreted as one variable

a1 = "font add kll alphabet".split()

cmd = cmd_parser(cmd_name, cmds)
print(cmd.parse(a1))
