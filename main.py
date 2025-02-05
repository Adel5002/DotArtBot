import asyncio
import base64
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
from io import BytesIO

from utils.forms import TakeImageFromUser
from utils.list_of_commands import commands
from utils.photo_to_dotart import make_b_and_w_image

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
    await state.update_data(image=message.photo[-1].file_id)  # Сохраняем только file_id
    data = await state.get_data()

    # Получаем file_id
    image_id = await bot.get_file(data['image'])
    image_path = image_id.file_path

    user_folder = f'users_images/{message.from_user.id}'
    image_filename = f"{message.message_id}.jpg"
    image_full_path = os.path.join(user_folder, image_filename)

    # Создаём папку, если её нет
    os.makedirs(user_folder, exist_ok=True)

    # Скачиваем файл
    await bot.download_file(image_path, image_full_path)

    await state.clear()
    await message.answer('Please wait a few seconds...')
    make_b_and_w_image(str(message.from_user.id))

    # Обрабатываем изображение
    # decoded_image = base64.b64decode(make_b_and_w_image(str(message.from_user.id)))
    #
    # # Открываем изображение корректно
    # image_io = BytesIO(decoded_image)
    #
    # await message.answer_photo(BufferedInputFile(image_io.read(), 'file.jpeg'))


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