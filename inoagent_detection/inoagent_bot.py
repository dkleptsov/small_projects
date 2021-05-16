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
from monitoring.check_new_inoagents import check_new_nko
from monitoring.check_new_inoagents import check_new_smi

if sys.platform == "win32":
    BOT_TOKEN = os.getenv("TESTFLIGHT_BOT")
    LOGS_PATH = r"D:/repos/small_projects/inoagent_detection/logs/inoagent_bot.log"
    PATTERN_DB =r"D:/repos/small_projects/inoagent_detection/patterns_db.csv"
    SUBS_DB = r"monitoring/subscribers.txt"
else:
    BOT_TOKEN = os.getenv("INOAGENT_BOT")
    LOGS_PATH = r"/home/small_projects/inoagent_detection/logs/inoagent_bot.log"
    PATTERN_DB =r"/home/small_projects/inoagent_detection/patterns_db.csv"
    SUBS_DB = r"monitoring/subscribers.txt"

ADMIN_NICK = "my_admin_1"
START_MSG = "Этот бот проверяет текст на наличие упоминаний организаций, \
которые признаны иностранными агентами в Российской Федерации. 🕵️"
CONTACTS_MSG = f"По всем вопросам пишите @{ADMIN_NICK}"
AWAIT_MSG = "Ваше сообщение получено, пожалуста, ожидайте ответа. 🤗"
NO_RES_MSG = f"Мы не нашли в тексте вашего сообщения упоминаний \
иностранных агентов 🤔. Если вам кажется, что мы что-то пропустили, \
пожалуйста, напишите об этом @{ADMIN_NICK}"
UNKN_CONTENT = "Этот бот умеет работать только с текстами. 😌"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btns_text = ('💡 Как это работает', '🤓 Контакты')
keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота."),
        BotCommand(command="/help", description="Свяжитесь с нами."),
                ]
    await bot.set_my_commands(commands)


async def monitor():
    nko_changes = check_new_nko()
    smi_changes = check_new_smi(rewrite=True)
    nko_added,nko_deleted = nko_changes.get('added'), nko_changes.get('deleted')
    smi_added,smi_deleted = smi_changes.get('added'), smi_changes.get('deleted')
    changes = ""    
    if nko_added:
        changes += f"В список иноагентов НКО добавлено:\n{nko_added}\n"
    if nko_deleted:
        changes += f"Из списка иноагентов НКО удалено:\n{nko_deleted}\n"
    if smi_added:
        changes += f"В список иноагентов СМИ добавлено:\n{smi_added}\n"
    if smi_deleted:
        changes += f"Из списка иноагентов СМИ удалено:\n{smi_deleted}"
    
    with open(SUBS_DB, "r", encoding="utf-8") as subs_file:
        subs_list = subs_file.readlines()
    
    if len(changes) > 0:
        for sub in subs_list:
            await bot.send_message(sub, changes)
    await asyncio.sleep(60)


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", retention="14 days"
              , serialize=True)

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.answer(START_MSG, reply_markup=keyboard_markup)
    
    @dp.message_handler(commands=['help'])
    async def help_message(message: types.Message):
        await message.answer(CONTACTS_MSG, reply_markup=keyboard_markup)
        
    @dp.message_handler(commands=['monitor'])
    async def monitor_message(message: types.Message):
        await bot.send_message(91675683, "Monitoring started!")
        while True:
            await monitor()

    @dp.message_handler(lambda message: message["text"] =="💡 Как это работает")
    async def how_it_works(message: types.Message):
        await message.answer(START_MSG, reply_markup=keyboard_markup)

    @dp.message_handler(lambda message: message["text"] == "🤓 Контакты")
    async def contact_us(message: types.Message):
        await message.answer(CONTACTS_MSG, reply_markup=keyboard_markup)

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
        log_entry = f"\nFrom id: {message['from']['id']}\
                      \nFrom nick: {message['from']['username']}\
                      \nText: {message['text']}\
                      \nNumber of detected inoagents: {len(results)}"
        logger.info(log_entry)
        await bot.send_message(91675683, log_entry)

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
