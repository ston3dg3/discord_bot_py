class MyFont:    

    fonts = []
    alphabet = "abcdefghijklmnoprstuwvxyz"

    def __init__(self, name, font_dict=None, trans_string=None) -> None:
        self.name = name
        self.font_dict=font_dict
        self.trans_string=trans_string
        
        if (font_dict is not None):
            self.trans_table = "".maketrans(font_dict)
            self.fancy_name = (name.lower()).translate(self.trans_table)
        elif (len(trans_string)==len(MyFont.alphabet)):
            self.trans_table = "".maketrans(MyFont.alphabet, trans_string)
            self.fancy_name = (name.lower()).translate(self.trans_table)
        else:
            self.trans_table = None
            self.fancy_name = None

        if any(x for x in MyFont.fonts if x.name==name):
            pass
        else:
            MyFont.fonts.append(self)

    def __str__(self):
        return f"Font: {self.fancy_name}"

    @classmethod
    def translator(cls, stringg, font_name):
        selected_font = None
        selected_font = [x for x in MyFont.fonts if x.name==font_name][0]
        if selected_font != None: 
            translated_text = (stringg.lower()).translate(selected_font.trans_table)
        else:
            translated_text = "No such font exists you dummy 🫠"
        return translated_text

    @classmethod
    def font_names(cls):
        names = [x.name for x in MyFont.fonts]
        return names
    
    @classmethod
    def fancy_font_names(cls):
        names = [x.fancy_name for x in MyFont.fonts]
        return names

    @classmethod
    def add_local_font(cls, row : tuple) -> None:
        name = row[0]
        trans_string = row[1] 
        if(name not in MyFont.font_names()):
            fontt = MyFont(name, trans_string=trans_string)
            return f"Font {fontt.fancy_font_names()[-1]} has been added"
        else:
            return "Fonts already in the list"







