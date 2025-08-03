from aiogram import Bot, Dispatcher

import config


bot = Bot(token=config.TGBOT_TOKEN)
dp = Dispatcher()


async def start_polling():
    from src.handlers import router

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
