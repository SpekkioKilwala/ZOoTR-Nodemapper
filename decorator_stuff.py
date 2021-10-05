
# Decorators are a bit of a mental jump.
# https://realpython.com/primer-on-python-decorators/
# They seem to be:
# A way to modify the behaviour of a given function.

# This ties into packages like Dash by letting you write simple functions,
# invoke the decorator upon them, and let the package deal with all the real
# work of making those functions do things like run web widgets or react to
# events like mouse clicks.

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")

say_whee()