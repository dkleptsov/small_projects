import os
import sys
from aiogram import Bot, Dispatcher, executor, types
import time
from loguru import logger
import gc
import schedule

LOGS_PATH = r"logs/getafterit_bot.log"
BOT_TOKEN = os.getenv("GETAFTERIT_BOT")
PRIVATE_MSG = "This bot is private."


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", retention="14 days"
            , serialize=True)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns_text = ('Done!', 'Failed!')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    

    @dp.message_handler()
    async def all_messages(message: types.Message):
        if message['from']['id'] != 91675683:
            await message.answer(PRIVATE_MSG)
            
        elif message["text"][:5] == 'Plan:':
            PLAN = message['text'][5:]
            with open("plan.txt", "w") as f:
                f.write(PLAN)
            await message.answer(f"Your plan is:{PLAN}")
            
        elif message["text"][:6] == 'Done!':
            with open("plan.txt") as f:
                PLAN  = f.read()
            await message.answer(f"You successfully done:\n{PLAN}")
        
        elif message["text"][:6] == 'Failed!':
            with open("plan.txt") as f:
                PLAN  = f.read()
            await message.answer(f"You failed:\n{PLAN}")
        
        else:
            await message.answer("Valid commands are:\
                \nPlan: your plan\nDone!\nFailed!")

        # await bot.send_message(91675683, "XXX")
    
    logger.info("Get after it bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)


if __name__ == '__main__':
    main()
