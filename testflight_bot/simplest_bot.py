"""
    This bot features:
    - catching commands start and help
    - reply - mentions oroginal message
    - answer - do not mention original message 

"""

import os
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=os.getenv('TESTFLIGHT_BOT'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    await message.reply("Hi! I'm a Bot!")


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.reply("Hi! I'm a Bot and I have the following commands:")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
