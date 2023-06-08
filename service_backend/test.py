from functools import wraps
from typing import Callable
token = {
    'name': 'paulon'
}
def decode_me(func: Callable):
    @wraps(func)
    def wrapper(token):
        
        if 'name' in token:
            your_name = token['name']
        else:
            your_name = 'none'

        return func(your_name)
    return wrapper

# @decode_me
def namename(my_name):
    return my_name

if __name__ == "__main__":
    print(namename(token))