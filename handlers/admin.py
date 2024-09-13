from create_bot import dp, bot
from aiogram import types, Dispatcher


async def admin_panel(message: types.Message):
    await bot.send_message(message.from_user.id, f'У вас не хватает прав для использования этой команды!')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=['ppp'])
