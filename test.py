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
from aiogram import types

from settings import ADMINS


