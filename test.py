# def my_decorator(func):
#     def wrapper():
#         func()
#         print("Что-то происходит до вызова функции.")
#         print("Что-то происходит после вызова функции.")
#     return wrapper
#
#
# @my_decorator
# def say_hello():
#     print("Hello!")
#
# say_hello()
# from aiogram import types pep8

# def s (a,b,*args):
#     print(args)
# s(1,2,3,4,5,6)
def a(age , **kwargs):
    print(kwargs)


a(name="Pasha", friend="Grisha")
