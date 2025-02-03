import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from dotenv import load_dotenv

from utils.forms import TakeImageFromUser
from utils.list_of_commands import commands

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Start command handler
@dp.message(CommandStart())
async def start_command_handler(message: types.Message) -> None:
    await message.answer(f'Hello dear, {html.bold(message.from_user.full_name)}!')

@dp.message(Command('upload_image'))
async def image_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(TakeImageFromUser.image)
    await message.answer(
        'Please upload an image',
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(TakeImageFromUser.image, F.photo)
async def get_photo(message: types.Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(image=message.photo)
    data = await state.get_data()
    image_id= await bot.get_file(data['image'][-1].file_id)
    image_path = image_id.file_path

    if os.path.exists(f'users_images/{message.from_user.id}'):
       await bot.download_file(image_path, f'users_images/{message.from_user.id}/{message.message_id}.jpg')
    else:
        os.mkdir(f'users_images/{message.from_user.id}')
        await bot.download_file(image_path, f'users_images/{message.from_user.id}/{message.message_id}.jpg')

    await state.clear()
    await message.answer('Please wait a second...')


@dp.message(TakeImageFromUser.image)
async def data_is_not_photo(message: types.Message, state: FSMContext):
    await message.reply("There's no image (ノಠ益ಠ)ノ彡┻━┻")
    await image_handler(message, state)


# Start bot
async def main() -> None:
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())