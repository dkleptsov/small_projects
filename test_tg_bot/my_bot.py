import os
# import sys
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("ABS_SUM_BOT_TOKEN")


def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    button_hi = KeyboardButton('Привет! 👋')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.reply("HELLO!", reply_markup=kb.greet_kb)

    @dp.message_handler()
    async def sum_message(message: types.Message):
        # Download, save, encode and send
        await message.answer(f"RESPONSE")

    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        print(e)
    return None


if __name__ == '__main__':
    main()


# Docs: https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html
