from Bot.core.handlers import router
from Bot.core.settings import TOKEN_ID
from aiogram import Bot, Dispatcher
import asyncio
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], ".."))
sys.path.append('/home/zetis/Документы/VScode/OCRP/SRC/Bot')


async def main():
    bot = Bot(token=TOKEN_ID, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Выход')
