import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import IDFilter
import time
from loguru import logger
import gc
import youtube_dl


ADMIN_ID = 91675683
LOGS_PATH = r"D:/repos/tmp/logs/my_yt_mp3.log"
MUSIC_PATH = r"D:/OneDrive/Media/NEW MUSIC/yt_bot/"
BOT_TOKEN = os.getenv("YT2DRIVE_BOT")
START_MSG = "This is private bot. 🔒"
AWAIT_MSG = "Your message has been received. Please wait for an answer. 🤗"

BAD_PATH_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
PARAMS = {'format': 'bestaudio/best', 'keepvideo': False, 'outtmpl': 'filename',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
    'preferredquality': '192',}]}

logger.add(LOGS_PATH, format="{time} {level} {message}",
               retention="14 days", serialize=True)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@logger.catch
def main():
    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.answer(START_MSG)

    @dp.message_handler(IDFilter(user_id=ADMIN_ID))
    async def all_messages(message: types.Message):
        if not (message["text"].startswith('https://www.youtube.com/')
                  or message["text"].startswith('https://youtu.be/')
                  or message["text"].startswith('youtu.be/')
                  or message["text"].startswith('youtube.com/')):
            await message.answer('Please enter valid Youtube link. For example:\
                https://www.youtube.com/watch?v=NUYvbT6vTPs')
        else:
            await message.answer(AWAIT_MSG)

            # Download, save, encode and send
            start = time.time()
            video_info = youtube_dl.YoutubeDL().extract_info(
                url=message["text"], download=False)
            video_info['title']= ''.join(i for i in video_info['title'][:99]
                                            if not i in BAD_PATH_CHARS)
            PARAMS['outtmpl'] = f"{MUSIC_PATH}{video_info['title']}.mp3"
            with youtube_dl.YoutubeDL(PARAMS) as ydl:
                ydl.download([video_info['webpage_url']])
            await bot.send_audio(message['from']['id'],
                                    audio=open(PARAMS['outtmpl'], 'rb'))
            response_time = f"{time.time() - start:.3f}"
            await message.answer(f"Response time: {response_time} sec")

            # Logging
            log_entry = f"\nMessage from: {message['from']['id']} \
                          \nTitle: {video_info['title']} \
                          \nResponse time: {response_time} sec"
            logger.info(log_entry)

            # Garbage collection
            gc.collect()

    logger.info("Youtube downloader bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)
    return None


if __name__ == '__main__':
    main()


# TODO:

