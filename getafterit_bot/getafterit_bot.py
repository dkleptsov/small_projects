import os
import sys
from aiogram import Bot, Dispatcher, executor, types
import time
from loguru import logger
import gc

LOGS_PATH = r"logs/getafterit_bot.log"
BOT_TOKEN = os.getenv("GETAFTERIT_BOT")
PRIVATE_MSG = "This bot is private."


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", retention="14 days"
            , serialize=True)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    # keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btns_text = ('💡 Как это работает', '🤓 Контакты')
    # keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.reply(PRIVATE_MSG)

    @dp.message_handler()
    async def sum_message(message: types.Message):
        if message['from']['id'] != 91675683:
            await message.answer(PRIVATE_MSG)
        else:
            await message.answer("Hello!")            
        # await bot.send_message(91675683, "XXX")

    @dp.message_handler(commands=['reminder'])
    async def process_start_command(message: types.Message):
        await bot.send_message(91675683, "test message")


    
    logger.info("Get after it bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)


if __name__ == '__main__':
    main()
