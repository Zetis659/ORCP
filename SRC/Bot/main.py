import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], ".."))
sys.path.append('/home/zetis/Документы/VScode/OCRP/SRC/Bot')
import asyncio
# from aiogram import Bot, Dispatcher, F
from aiogram import Bot, Dispatcher
# from aiogram.types import Message, CallbackQuery
# import Bot.core.keyboards as kb
from Bot.core.settings import TOKEN_ID
from Bot.core.handlers import router



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
