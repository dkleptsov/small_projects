import os
import sys
from aiogram import Bot, Dispatcher, executor, types
import time
from loguru import logger
import gc
import youtube_dl

LOGS_PATH = r"D:/repos/small_projects/yt_downloader/logs/yt_mp3_download.log"
MUSIC_PATH = r"D:/OneDrive/Media/NEW MUSIC/yt_bot/"

BOT_TOKEN = os.getenv("TESTFLIGHT_BOT") #os.getenv("YT_MP3_DOWNLOAD_BOT_TOKEN")
START_MSG = "This bot downloads mp3 from youtube videos. 🤩"
AWAIT_MSG = "Your message has been received. Please wait for an answer. 🤗"

BAD_PATH_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
PARAMS = {'format': 'bestaudio/best', 'keepvideo': False, 'outtmpl': 'filename',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
    'preferredquality': '192',}]}

@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}",
               retention="14 days", serialize=True)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns_text = ('💡 How this bot works', '🤓 Contact us')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.reply(START_MSG, reply_markup=keyboard_markup)

    @dp.message_handler()
    async def sum_message(message: types.Message):
        if message["text"] == '💡 How this bot works':
            await message.answer(START_MSG, reply_markup=keyboard_markup)
        elif message["text"] == '🤓 Contact us':
            await message.answer('This bot created by @real_den',
                                 reply_markup=keyboard_markup)
        elif not (message["text"].startswith('https://www.youtube.com/')
                  or message["text"].startswith('https://youtu.be/')
                  or message["text"].startswith('youtu.be/')
                  or message["text"].startswith('youtube.com/')):
            await message.answer('Please enter valid Youtube link. For example:\
                https://www.youtube.com/watch?v=NUYvbT6vTPs',
                reply_markup=keyboard_markup)
        else:
            await message.answer(AWAIT_MSG, reply_markup=keyboard_markup)

            # Download, save, encode and send
            start = time.time()
            video_info = youtube_dl.YoutubeDL().extract_info(
                url=message["text"], download=False)
            if video_info['duration']>600 and message['from']['id'] != 91675683:
                await message.answer("Song is longer than 10 minutes. \
                    Please contact @real_den", reply_markup=keyboard_markup)
                response_time = 0
            else:
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
            await bot.send_message(91675683, log_entry)

            # Deleting unwanted music my id 91675683
            mp3_exists =os.path.exists(f"{MUSIC_PATH}{video_info['title']}.mp3")
            if message['from']['id'] != 91675683 and mp3_exists:
                os.remove(f"{MUSIC_PATH}{video_info['title']}.mp3")

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
# Перенести все if про текст в отдельные функции
