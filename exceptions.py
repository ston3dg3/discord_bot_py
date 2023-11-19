class DatabaseNoneType(Exception):
    pass
    # raise when object passed to a database is of type None


class CommandArgsWrongType(Exception):
    def __init__(self, message="command_parser.py received wrong types of arguments!"):
        self.message = message
        super().__init__(self.message)


class ParsingTooManyDelimeters(Exception):
    def __init__(self, message = "The arugment you provided has too many delimeters :") -> None:
        self.message = message
        super().__init__(self.message)


class ParsingLenghtInvalid(Exception):
    def __init__(self, message = "Length of the provided argument does not match the required argument length") -> None:
        self.message = message
        super().__init__(self.message)