import os
import sys
from aiogram import Bot, Dispatcher, executor, types
import time
from loguru import logger
from test_pattern import check_all_patterns
import gc

LOGS_PATH = r"/logs/inoagent_bot.log"
BOT_TOKEN = os.getenv("INOAGENT_BOT")
START_MSG = "Этот бот проверяет текст на наличие упоминаний организаций, \
которые признаны иностранными агентами в Российской Федерации. 🕵️"
CONTACTS_MSG = "По всем вопросам пишите @real_den"
AWAIT_MSG = "Ваше сообщение получено, пожалуста, ожидайте ответа. 🤗"


@logger.catch
def main():
    logger.add(LOGS_PATH, format="{time} {level} {message}", retention="14 days"
               , serialize=True)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns_text = ('💡 Как это работает', '🤓 Контакты')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    @dp.message_handler(commands=['start'])
    async def start_message(message: types.Message):
        await message.reply(START_MSG, reply_markup=keyboard_markup)

    @dp.message_handler()
    async def sum_message(message: types.Message):
        if message["text"] == '💡 Как это работает':
            await message.answer(START_MSG, reply_markup=keyboard_markup)
        elif message["text"] == '🤓 Контакты':
            await message.answer(CONTACTS_MSG, reply_markup=keyboard_markup)
        else:
            await message.answer(AWAIT_MSG, reply_markup=keyboard_markup)

        start = time.time()
        results = check_all_patterns(message["text"])
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
        # Logging
        log_entry = f"\nMessage from: {message['from']['id']}\
                      \nText: {message['text']}\
                      \nNumber of detected inoagents: {len(results)}"
        logger.info(log_entry)
        await bot.send_message(91675683, log_entry)

        # Garbage collection
        gc.collect()

    logger.info("Inoagent bot started!")
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logger.error(e)
        time.sleep(15)
    return None


if __name__ == '__main__':
    main()
