import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.handlers.common import register_handlers_common
from app.handlers.morning import register_handlers_morning


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Bot welcome message."),
        BotCommand(command="/help", description="Bot help."),
        BotCommand(command="/settings", description="Bot settings."),
        BotCommand(command="/morning", description="Secret morning check-list"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("My morning check list bot started!")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=os.getenv('TESTFLIGHT_BOT'))
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp, 91675683)
    register_handlers_morning(dp, 91675683)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
