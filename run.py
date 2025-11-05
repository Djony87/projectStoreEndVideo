import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.hendlers import router
from app.database.models import async_main #, add_columns_to_users

async def main():
    await async_main()
    #await add_columns_to_users()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
