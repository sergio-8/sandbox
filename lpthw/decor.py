import sys
from sys import argv



def log_function_call(func):
    def wrapper(*args, **kwargs ):
        print('calling function  {} with args {} and kwargs {}'.format(func.__name__, args, kwargs))
        return func(*args, **kwargs)
    return wrapper()

@log_function_call
def foo(x, y):
    print(x+y)
    return x+y







