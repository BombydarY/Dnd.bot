import json

from create_bot import dp, bot
from aiogram import types, Dispatcher

from decorators import admin_check, error_check
from neur import get_answer_gpt, pic_make

USER_HELP_MADE = {}
ALL_USERS = []


@error_check
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, "Hello\n"
                                                 "/help_story_made\n"
                                                 "/help_person_made")
    with open('Peoples.json','r') as f:
        users:list = json.load(f)
        ids = [list(f.keys())[0] for f in users]
        if str(message.from_user.id) not in ids:
            users.append({message.from_user.id:message.from_user.username})
        else:
            return


    with open('Peoples.json','w') as f:
        json.dump(users, f)



@error_check
async def help_story_made(message: types.Message):
    await bot.send_message(message.from_user.id, "Мне нужно описание истории которую ты хочешь придумать")

    USER_HELP_MADE[message.from_user.id] = {"message_user": "", "state": 1}
    print(USER_HELP_MADE)


@error_check
async def help_person_made(message: types.Message):
    await bot.send_message(message.from_user.id, "Мне нужно описание персонажа которого ты хочешь придумать")

    USER_HELP_MADE[message.from_user.id] = {"message_user": "", "state": 2}
    print(USER_HELP_MADE)


@error_check
async def no(message: types.Message):
    await bot.send_message(message.from_user.id, "Ты бяка")


@error_check
async def text_handler(message: types.Message):
    if message.from_user.id in USER_HELP_MADE:
        state = USER_HELP_MADE[message.from_user.id]["state"]
        print(message.text, state)
        if state == 1:
            USER_HELP_MADE[message.from_user.id]["message_user"] = message.text
            answer = await get_answer_gpt(
                promt="Ты разбираешься в настольных играх (игра DND), очень круто скреативь и придумай историю на следующую тему",
                quastion=message.text)
            await bot.send_message(message.from_user.id, answer)
            del USER_HELP_MADE[message.from_user.id]
        if state == 2:
            USER_HELP_MADE[message.from_user.id]["message_user"] = message.text
            answer = await get_answer_gpt(
                promt="Ты разбираешься в настольных играх (игра DND), очень круто скреативь и придумай персонажа на следующую тему",
                quastion=message.text)
            await bot.send_message(message.from_user.id, answer)
            await bot.send_message(message.from_user.id, "You want see your person?/yes /no")


@error_check
async def yes(message: types.Message):
    state = USER_HELP_MADE[message.from_user.id]["state"]
    if message.from_user.id in USER_HELP_MADE and state == 2:
        picture = await pic_make(promt=USER_HELP_MADE[message.from_user.id]["message_user"])
        await bot.send_photo(message.from_user.id, photo=picture)
        del USER_HELP_MADE[message.from_user.id]
    else:
        await bot.send_message(message.from_user.id, "Вы не начали придумывать персонажа /help_person_made")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(help_story_made, commands=['help_story_made'])
    dp.register_message_handler(help_person_made, commands=['help_person_made'])
    dp.register_message_handler(yes, commands=["yes"])
    dp.register_message_handler(no, commands=["no"])
    dp.register_message_handler(text_handler, content_types=["text"])
