import os
from aiogram import Bot, Dispatcher, executor, types
import time
from loguru import logger
import gc

BOT_TOKEN = os.getenv("YT_MP3_DOWNLOAD_BOT_API_KEY")
START_MSG = "This bot downloads mp3 from youtube videos"
LOGS_PATH = r"logs/yt_mp3_download.log"


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", retention="14 days", serialize=True)  # Logging
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.reply(START_MSG)

    @dp.message_handler()
    async def sum_message(message: types.Message):
        start = time.time()
        # Input magic here
        response_time = f"{time.time() - start:.3f}"
        await message.answer(f"Response time: {response_time} sec")
        log_entry = f"\nMessage from: {message['from']['username']} \nResponse time: {response_time} sec"
        logger.info(log_entry)
        await bot.send_message(91675683, log_entry)
        gc.collect()  # Garbage collection

    logger.info("Youtube downloader bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)
    return None


if __name__ == '__main__':
    main()


# Docs:
