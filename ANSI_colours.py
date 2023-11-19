class ANSI:
                
    @classmethod
    def text_colour(self,text, color):

        def get_result_string(color_code): return f"\u001b[0;{color_code}m{text}\u001b[0;0m"

        if color == "grey" or color == "gray":
            return get_result_string(30)
        elif color == "red":
            return get_result_string(31)
        elif color == "green":
            return get_result_string(32)
        elif color == "yellow":
            return get_result_string(33)
        elif color == "blue":
            return get_result_string(34)
        elif color == "pink":
            return get_result_string(35)
        elif color == "cyan":
            return get_result_string(36)
        elif color == "white":
            return get_result_string(37)
        else:
            return text
        
    @classmethod
    def background_color(self, text, color):

        def get_result_string(color_code): return f"\u001b[0;{color_code}m{text}\u001b[0;0m"

        if color == "Dblue" or color == "dark_blue":
            return get_result_string(40)
        elif color == "orange":
            return get_result_string(41)
        elif color == "Lblue":
            return get_result_string(42)
        elif color == "turqoise":
            return get_result_string(43)
        elif color == "Dgray" or color == "Dgrey":
            return get_result_string(44)
        elif color == "indigo":
            return get_result_string(45)
        elif color == "Lgrey" or color == "Lgray":
            return get_result_string(46)
        elif color == "white":
            return get_result_string(47)
        else:
            return text
        
    @classmethod
    def wrapANSIblock(self, text: str) -> str:
        return f"""```ansi\n"""+text+"""\n```"""

        





