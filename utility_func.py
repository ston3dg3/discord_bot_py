# File containing utility functions for manipulating strings etc...
import json
import re
from bot_setup import bot_parameters
from database_test import updateMessage

class utilities:

    @classmethod
    def add_word_to_count(self, new_word):
        count_word = {
            "word": new_word,
            "count": 0
        }
        json_obj = json.dump(count_word, indent=4)
        file = open("word_count.txt", "a")
        file.write(json_obj)
        file.close()

    @classmethod
    def swear_word(self, message):
        msg = message.content
        return any(ele in msg for ele in bot_parameters.swear_words)

    @classmethod
    def count_word(self, message, mess_list):
        # upper matching also indcludes elements within other strings.
        # matching_element = next((element for element in mess_list if element in message.content), None)
        matching_element = next((element for element in mess_list if re.search(rf'\b{element}\b', message.content)), None)
        if matching_element:
            updateMessage(matching_element)

    @classmethod
    def add_to_txt(self, message):
        msg = message.content
        f = open('fav_list.txt', 'a')
        f.write(msg)
        f.write('\n')
        f.close()

    @classmethod
    def clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)