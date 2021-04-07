"""
    My check list bot, features:
    - Scheduled notifications
    
"""

import os
import time
import asyncio
import aioschedule
from aiogram import Bot, Dispatcher, executor, types
import random

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
    

##### Scheduled part of the bot
@dp.message_handler()
async def morning_task():
    await bot.send_message(91675683, "It's time for morning check-list!")
    

@dp.message_handler()
async def test_task(hour):
    now = time.strftime("%H:%M:%S", time.localtime()) + hour
    print(now)
    await bot.send_message(91675683, now)


async def scheduler():
    # aioschedule.every().day.at("7:00").do(morning_task)
    # aioschedule.every(3).seconds.do(noon_print)
    # aioschedule.every().day.at("23:44").do(test_task, "23 hour")

    aioschedule.every().day.at("7:00").do(morning_task)
        
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
