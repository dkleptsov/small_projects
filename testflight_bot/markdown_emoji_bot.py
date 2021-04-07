"""
    This bot features:
    - send messages with markdown
    - send emoji (names: https://www.webfx.com/tools/emoji-cheat-sheet/)
    - catching unknown content
    - simple logging
"""

import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode


logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TESTFLIGHT_BOT'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    await message.reply("Hi! I'm a Bot!")


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.reply("I have the following commands:\nstart\nhelp\ntest")
    
    
@dp.message_handler(commands=['test'])
async def test_message(message: types.Message):
    msg = text(emojize(":green_book: :blue_book: :closed_book: :gem: :dragon:"),
               bold('Bold text'), italic('Italic text'), code('command'),
               pre("pre('pre')"), 'normal text', 'separator', 'test', sep='\n')
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
    

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_content(message: types.Message):
    message_text = text(emojize("I don't know what to do :astonished:"),
                italic('\nI just remind'), 'about', '/help', code('command'))
    await message.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
