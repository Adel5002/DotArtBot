import os
import base64

from io import BytesIO
from PIL import Image

def make_b_and_w_image(user_id: str) -> str:
    path_to_images = os.path.join('users_images', user_id)
    images_list = sorted(os.listdir(path_to_images))  # Сортируем файлы, чтобы брать последний загруженный

    if not images_list:
        raise FileNotFoundError("Нет изображений для обработки.")

    img_path = os.path.join(path_to_images, images_list[-1])
    img = Image.open(img_path)
    img = img.convert('L')
    img = img.point(lambda x: 255 if x > 100 else 0)

    # Кодируем изображение в base64
    buffered = BytesIO()
    img.save(buffered, format='JPEG')
    return base64.b64encode(buffered.getvalue()).decode()


