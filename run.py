import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import  load_dotenv


from app.hendlers import router
from app.admins.admin_hendlers import admin_router
from app.database.models import async_main #, add_columns_to_users

async def main():
    await async_main()
    #await add_columns_to_users()
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(router, admin_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
