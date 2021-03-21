import os
import gc
import sys
import time
import youtube_dl
from loguru import logger
from asgiref.sync import sync_to_async
from aiogram import Bot, Dispatcher, executor, types
from django.core.management.base import BaseCommand
from django.conf import settings
from ugc.models import Message
from ugc.models import Profile


BOT_TOKEN = os.getenv("TEST_FLIGHT_BOT")
LOGS_PATH = r"D:/small_projects/yt_downloader/logs/yt_mp3_download.log"
MUSIC_PATH = r"D:/OneDrive/Media/NEW MUSIC/yt_bot/"
START_MSG = "This bot downloads mp3 from youtube videos. 🤩"
AWAIT_MSG = "Your message has been received. Please wait for an answer. 🤗"

BAD_PATH_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
PARAMS = {'format': 'bestaudio/best', 'keepvideo': False, 'outtmpl': 'filename',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3',
    'preferredquality': '192',}]}


@sync_to_async
def save_to_db(user_id, user_name, user_message):
    db_id, _ = Profile.objects.get_or_create(external_id=user_id,
    defaults={'name': user_name,})
    m = Message(profile = db_id, text = user_message,)
    m.save()
    d_count = Message.objects.filter(profile=db_id).count()
    print (d_count)
    return d_count


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", 
               retention="14 days", serialize=True)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns_text = ("💡 How this bot works", "🤓 Contact us")
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.reply(START_MSG, reply_markup=keyboard_markup)

    @dp.message_handler()
    async def all_messages(message: types.Message):
        user_id = message['from']['id']
        user_message = message["text"]
        if message['from']['username']:
            user_name = message['from']['username']
        else:
            user_name = "undefined"

        if user_message == "💡 How this bot works":
            await message.answer(START_MSG, reply_markup=keyboard_markup)
        elif user_message == "🤓 Contact us":
            await message.answer("This bot created by @real_den", 
                                 reply_markup=keyboard_markup)
        elif not (user_message.startswith('https://www.youtube.com/') 
                  or user_message.startswith('https://youtu.be/') 
                  or user_message.startswith('youtu.be/') 
                  or user_message.startswith('youtube.com/')):
            await message.answer('Please enter valid Youtube link. For example:\
                https://www.youtube.com/watch?v=NUYvbT6vTPs', 
                reply_markup=keyboard_markup)
        else:
            await message.answer(AWAIT_MSG, reply_markup=keyboard_markup)

            # Download, save, encode and send
            start = time.time()
            video_info = youtube_dl.YoutubeDL().extract_info(
                url=user_message, download=False)
            if video_info['duration']>600 and user_id != 91675683:
                await message.answer("Song is longer than 10 minutes. \
                    Please contact @real_den", reply_markup=keyboard_markup)
                response_time = 0
            else:
                video_info['title']= ''.join(i for i in video_info['title'][:99] 
                                              if not i in BAD_PATH_CHARS)
                PARAMS['outtmpl'] = f"{MUSIC_PATH}{video_info['title']}.mp3"
                with youtube_dl.YoutubeDL(PARAMS) as ydl:
                    ydl.download([video_info['webpage_url']])
                await bot.send_audio(user_id,audio=open(PARAMS['outtmpl'],'rb'))
                response_time = f"{time.time() - start:.3f}"
                await message.answer(f"Response time: {response_time} sec")
                
                # Logging                
                counter = await save_to_db(user_id, user_name, user_message)
                entry = f"\nnick: {user_name} id: {user_id} counter: {counter}"
                logger.info(entry)
                await bot.send_message(91675683, entry)                                
                
            # Deleting unwanted music my id 91675683
            mp3_exists =os.path.exists(f"{MUSIC_PATH}{video_info['title']}.mp3")
            if user_id != 91675683 and mp3_exists:
                os.remove(f"{MUSIC_PATH}{video_info['title']}.mp3")

            # Garbage collection
            gc.collect()

    logger.info("Youtube downloader bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)


class Command(BaseCommand):
    help = 'aiogram telegram bot for downloading youtube videos'

    def handle(self, *args, **options):
        main()
        