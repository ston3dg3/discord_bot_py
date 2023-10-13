# File containing utility functions for manipulating strings etc...
import json
import re
from database_test import updateMessage
import time
from datetime import datetime

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
    from bot_setup import bot_parameters
    msg = message.content
    return any(ele in msg for ele in bot_parameters.swear_words)


def count_word( message, mess_list):
    # upper matching also indcludes elements within other strings.
    # matching_element = next((element for element in mess_list if element in message.content), None)
    matching_element = next((element for element in mess_list if re.search(rf'\b{element}\b', message.content)), None)
    if matching_element:
        updateMessage(matching_element)


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