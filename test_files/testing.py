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


