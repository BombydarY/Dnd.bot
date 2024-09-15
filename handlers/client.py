from create_bot import dp, bot
from aiogram import types, Dispatcher

from decorators import admin_check, error_check
from neur import get_answer_gpt


USER_HELP_MADE = {}

@error_check
@admin_check
async def send_welcome(message: types.Message):
    raise IndexError
    await bot.send_message(message.from_user.id, "Hello\n"
                                                 "/help_story_made\n"
                                                 "/help_person_made")


async def help_story_made(message: types.Message):
    await bot.send_message(message.from_user.id, "Мне нужно описание истории которую ты хочешь придумать")

    USER_HELP_MADE[message.from_user.id] = {"message_user": "", "state": 1}
    print(USER_HELP_MADE)


async def help_person_made(message: types.Message):
    await bot.send_message(message.from_user.id, "Мне нужно описание персонажа которого ты хочешь придумать")

    USER_HELP_MADE[message.from_user.id] = {"message_user": "", "state": 2}
    print(USER_HELP_MADE)


async def text_handler(message: types.Message):
    if message.from_user.id in USER_HELP_MADE:
        state = USER_HELP_MADE[message.from_user.id]["state"]
        print(message.text, state)
        if state == 1:
            USER_HELP_MADE[message.from_user.id]["message_user"] = message.text
            answer = get_answer_gpt(
                promt="Ты разбираешься в настольных играх (игра DND), очень круто скреативь и придумай историю на следующую тему",
                quastion=message.text)
            await bot.send_message(message.from_user.id, answer)
            del USER_HELP_MADE[message.from_user.id]
        if state == 2:
            USER_HELP_MADE[message.from_user.id]["message_user"] = message.text
            answer = get_answer_gpt(
                promt="Ты разбираешься в настольных играх (игра DND), очень круто скреативь и придумай персонажа на следующую тему",
                quastion=message.text)
            await bot.send_message(message.from_user.id, answer)
            del USER_HELP_MADE[message.from_user.id]



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(help_story_made, commands=['help_story_made'])
    dp.register_message_handler(help_person_made, commands=['help_person_made'])
    dp.register_message_handler(text_handler, content_types=["text"])
