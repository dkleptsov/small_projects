#!/usr/bin/python3
import os
import sys
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import time
from loguru import logger
from test_pattern import check_all_patterns
import gc

LOGS_PATH = r"/home/small_projects/inoagent_detection/logs/inoagent_bot.log"
PATTERN_DB =r"/home/small_projects/inoagent_detection/patterns_db.csv"
#r"D:/small_projects/inoagent_detection/patterns_db.csv")
ADMIN_NICK = "real_den"
BOT_TOKEN = os.getenv("INOAGENT_BOT") #os.getenv("TESTFLIGHT_BOT") #
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


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", retention="14 days"
              , serialize=True)

    async def set_commands(bot: Bot):
        commands = [
            BotCommand(command="/start", description="Запустить бота."),
            BotCommand(command="/help", description="Свяжитесь с нами."),
                    ]
        await bot.set_my_commands(commands)

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.reply(START_MSG, reply_markup=keyboard_markup)
    
    @dp.message_handler(commands=['help'])
    async def start_message(message: types.Message):
        await message.reply(CONTACTS_MSG, reply_markup=keyboard_markup)

    @dp.message_handler(lambda message: message["text"] =="💡 Как это работает")
    async def how_it_works(message: types.Message):
        await message.answer(START_MSG, reply_markup=keyboard_markup)

    @dp.message_handler(lambda message: message["text"] == "🤓 Контакты")
    async def contact_us(message: types.Message):
        await message.answer(CONTACTS_MSG, reply_markup=keyboard_markup)

    @dp.message_handler()
    async def sum_message(message: types.Message):
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
                    \nДата включения в реестр: {results[i]['date']}")
            await message.answer(
                f"Время обработки: {time.time() - start:.3f} секунд")
        else:
            await message.answer(NO_RES_MSG + 
            f"\nВремя обработки: {time.time() - start:.3f} секунд")

        # Logging
        log_entry = f"\nMessage from: {message['from']['id']}\
                      \nText: {message['text']}\
                      \nNumber of detected inoagents: {len(results)}"
        logger.info(log_entry)
        await bot.send_message(91675683, log_entry)

        # Garbage collection
        gc.collect()
    
    @dp.message_handler(content_types=ContentType.ANY)
    async def unknown_content(message: types.Message):
        await message.reply(UNKN_CONTENT)

    logger.info("Inoagent bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)
    return None


if __name__ == '__main__':
    main()
