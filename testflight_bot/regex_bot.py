"""
    This bot features:
    - logging
    - catching messages with regex
    - short way of sending photo
"""

import os
import logging
from aiogram import Bot, Dispatcher, executor, types

CATS = 'D:/repos/light_bots/testflight_bot/media_bot/media/pics/cats.jpg'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TESTFLIGHT_BOT'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    await message.reply("Hi! I'm a Bot!")


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.reply("Hi! I'm a Bot and I have the following commands:")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open(CATS, 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)