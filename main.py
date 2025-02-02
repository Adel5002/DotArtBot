import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv, dotenv_values

load_dotenv()

TOKEN = os.getenv('TOKEN')
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.answer(f'Hello dear, {html.bold(message.from_user.full_name)}!')

@dp.message()
async def message_handler(message: types.Message) -> None:
    await message.answer(text='Huh?')


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())