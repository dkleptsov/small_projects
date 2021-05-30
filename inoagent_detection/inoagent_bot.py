#!/usr/bin/python3
import os
import gc
import sys
import time
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import BotCommand
from aiogram.types.message import ContentType
from loguru import logger
from check_inoagent import check_all_patterns
from monitoring.check_new_orgs import check_all_orgs
from monitoring.check_pc import health


if sys.platform == "win32":
    BOT_TOKEN = os.getenv("TESTFLIGHT_BOT")
    BASE_PATH = r"D:/repos/small_projects/inoagent_detection/"
    LOGS_PATH = BASE_PATH + r"logs/inoagent_bot.log"
    PATTERN_DB = BASE_PATH + r"patterns_db.csv"
    SUBS_DB = BASE_PATH + r"monitoring/subscribers.txt"
else:
    BOT_TOKEN = os.getenv("INOAGENT_BOT")
    LOGS_PATH = r"/home/small_projects/inoagent_detection/logs/inoagent_bot.log"
    PATTERN_DB =r"/home/small_projects/inoagent_detection/patterns_db.csv"
    SUBS_DB = r"/home/small_projects/inoagent_detection/monitoring/subscribers.txt"

ADMIN_NICK = "my_admin_1"
LOGGING_ID = 1631744908
START_MSG = f"🕵️ Пришлите боту любой текст, а он проверит его на наличие \
имен организаций, которые признаны иностранными агентами в РФ.\n\n\
🔔 Подписаться - получать уведомления, об изменениях в реестрах \
организаций:\n\n\
Иноагентов СМИ: https://minjust.gov.ru/ru/documents/7755/ \n\
Иноагентов НКО: http://unro.minjust.ru/NKOForeignAgent.aspx\n\
Экстремистских: https://minjust.gov.ru/ru/documents/7822/\n\
Террористических: http://www.fsb.ru/fsb/npd/terror.htm\n\
Нежелательных: https://minjust.gov.ru/ru/documents/7756/\n\n\
🤓 По всем вопросам пишите @{ADMIN_NICK}"
AWAIT_MSG = "Ваше сообщение получено, пожалуста, ожидайте ответа. 🤗"
NO_RES_MSG = f"Мы не нашли в тексте вашего сообщения упоминаний \
иностранных агентов 🤔. Если вам кажется, что мы что-то пропустили, \
пожалуйста, напишите об этом @{ADMIN_NICK}"
UNKN_CONTENT = "Этот бот умеет работать только с текстами. 😌"
SUBSCRIBE_MSG = "Вы успешно подписались на уведомления об изменении списка \
иностранных агетов. 🤗"
UNSUBSCRIBE_MSG = "Вы успешно отписались от уведомлений об изменении списка \
иностранных агетов. 🤗"
SUBSCRIBED_MSG = "Вы уже подписаны на уведомления об изменении списка \
иностранных агетов. 🤗"
NOT_SUBSCRIBED_MSG = "Вы не подписаны на уведомления об изменении списка \
иностранных агетов. 🤗"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btns_text = ('💡 Как это работает', '🔔 Подписаться', '🔕 Отписаться')
keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота."),
        BotCommand(command="/help", description="Как это работает."),     
                ]
    await bot.set_my_commands(commands)


async def monitor():
    changes, downloads_status = check_all_orgs(rewrite=False)

    with open(SUBS_DB, "r", encoding="utf-8") as subs_file:
        subs_list = subs_file.readlines()
    
    if len(changes) > 0:
        for sub in subs_list:
            await bot.send_message(sub, changes, reply_markup=keyboard_markup,
            disable_web_page_preview=True)
    
    # Logging
    log_message = f"Success! Resources used: {health()}\
    \nDownload status: {downloads_status}"
    await bot.send_message(LOGGING_ID, log_message)
    logger.info(log_message)
    
    gc.collect()
    await asyncio.sleep(1200)


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", serialize=True)

    @dp.message_handler(commands=['start', 'help', 'settings'])
    async def start_message(message: types.Message):
        await message.answer(START_MSG, reply_markup=keyboard_markup,
        disable_web_page_preview=True)


    @dp.message_handler(commands=['reboot'])
    async def reboot_message(message: types.Message):
        await bot.send_message(LOGGING_ID, "Server will reboot!")
        os.system("reboot")


    @dp.message_handler(commands=['health'])
    async def health_message(message: types.Message):
        await bot.send_message(LOGGING_ID, health())


    @dp.message_handler(commands=['monitor'])
    async def monitor_message(message: types.Message):
        await bot.send_message(LOGGING_ID, "Monitoring launched!")
        logger.info("Monitoring launched!")
        while True:
            try:
                await monitor()
            except:
                log_message = f"FAILED! Resources used: {health()}"
                logger.info(log_message)
                await bot.send_message(LOGGING_ID, log_message)
                await asyncio.sleep(60)
                gc.collect()
        # else:
        #     await message.answer("Monitoring already active",
        #     reply_markup=keyboard_markup)


    @dp.message_handler(lambda message: message["text"] == '🔔 Подписаться')
    async def subscribe_message(message: types.Message):
        with open(SUBS_DB, "r", encoding="utf-8") as subs_file:
            subs_list = subs_file.readlines()
        new_sub = str(message['from']['id']) + "\n"
        if new_sub in subs_list:
            await message.answer(SUBSCRIBED_MSG, reply_markup=keyboard_markup)
        else:
            subs_list.append(new_sub)
            with open(SUBS_DB, "a", encoding="utf-8") as subs_file:
                subs_file.write(new_sub)            
            await message.answer(SUBSCRIBE_MSG, reply_markup=keyboard_markup)
            
            # Logging
            log_message = f"New subscriber! \nid: {message['from']['id']}\
            \nnick: {message['from']['username']}\n Current list: {subs_list}"
            logger.info(log_message)
            await bot.send_message(LOGGING_ID, log_message)


    @dp.message_handler(lambda message: message["text"] == '🔕 Отписаться')
    async def unsubscribe_message(message: types.Message):
        with open(SUBS_DB, "r", encoding="utf-8") as subs_file:
            subs_list = subs_file.readlines()
        new_sub = str(message['from']['id']) + "\n"
        if new_sub in subs_list:
            subs_list = set(subs_list)
            subs_list.remove(new_sub)
            with open(SUBS_DB, "w", encoding="utf-8") as subs_file:
                subs_file.writelines(subs_list)
            await message.answer(UNSUBSCRIBE_MSG, reply_markup=keyboard_markup)
            await bot.send_message(LOGGING_ID, 
            f"Subscriber removed! \nid: {message['from']['id']}\
            \nnick: {message['from']['username']}\
            \n Current list: {subs_list}")
        else:
            await message.answer(NOT_SUBSCRIBED_MSG, reply_markup=keyboard_markup)         


    @dp.message_handler(lambda message: message["text"] =="💡 Как это работает")
    async def how_it_works(message: types.Message):
        await message.answer(START_MSG, reply_markup=keyboard_markup, 
        disable_web_page_preview=True)


    @dp.message_handler()
    async def all_messages(message: types.Message):
        await set_commands(bot)
        await message.answer(AWAIT_MSG, reply_markup=keyboard_markup)
        start = time.time()
        results = check_all_patterns(message["text"], 
        patterns_db=PATTERN_DB)
        if len(results) > 0:
            for i in range(len(results)):
                await message.answer(
                f"Мы нашли текст: {results[i]['text_found']}\
                \nНазвание иноагента: {results[i]['name']}\
                \nТип иноагента: {results[i]['inoagent_type']}\
                \nПравовая форма иноагента: {results[i]['org_type']}\
                \nДата включения в реестр: {results[i]['date']}\
                \nИсключен ли иноагент из реестра: {results[i]['excluded']}")
            await message.answer(
                f"Время обработки: {time.time() - start:.3f} секунд")
        else:
            await message.answer(NO_RES_MSG + 
            f"\nВремя обработки: {time.time() - start:.3f} секунд")

        # Logging
        log_message = f"\nFrom id: {message['from']['id']}\
                      \nFrom nick: {message['from']['username']}\
                      \nText: {message['text']}\
                      \nNumber of detected inoagents: {len(results)}"
        logger.info(log_message)
        await bot.send_message(LOGGING_ID, log_message)

        # Garbage collection
        gc.collect()


    @dp.message_handler(content_types=ContentType.ANY)
    async def unknown_content(message: types.Message):
        await message.answer(UNKN_CONTENT)

    logger.info("Inoagent bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)
    return None


if __name__ == '__main__':
    main()
